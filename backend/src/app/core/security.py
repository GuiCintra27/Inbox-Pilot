from __future__ import annotations

import json
import logging
import threading
import time
from collections import Counter, defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.core.config import get_settings

logger = logging.getLogger("app.security")

TimeCallable = Callable[[], float]


@dataclass(frozen=True, slots=True)
class RateLimitDecision:
    allowed: bool
    retry_after_seconds: int = 0


@dataclass(frozen=True, slots=True)
class CircuitStateSnapshot:
    state: str
    opened_until: float | None
    consecutive_failures: int


class InMemoryRateLimiter:
    def __init__(self, *, clock: TimeCallable | None = None) -> None:
        self._clock = clock or time.monotonic
        self._buckets: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str, *, limit: int, window_seconds: int) -> RateLimitDecision:
        now = self._clock()

        with self._lock:
            bucket = self._buckets[key]
            while bucket and now - bucket[0] >= window_seconds:
                bucket.popleft()

            if len(bucket) >= limit:
                retry_after = max(1, int(window_seconds - (now - bucket[0])))
                return RateLimitDecision(allowed=False, retry_after_seconds=retry_after)

            bucket.append(now)
            return RateLimitDecision(allowed=True, retry_after_seconds=0)

    def reset(self) -> None:
        with self._lock:
            self._buckets.clear()


class InMemoryCircuitBreakerRegistry:
    def __init__(self, *, clock: TimeCallable | None = None) -> None:
        self._clock = clock or time.time
        self._state: dict[str, dict[str, float | int | None]] = defaultdict(
            lambda: {
                "consecutive_failures": 0,
                "opened_until": None,
            }
        )
        self._lock = threading.Lock()

    def is_open(self, provider_name: str) -> bool:
        now = self._clock()
        with self._lock:
            state = self._state[provider_name]
            opened_until = state["opened_until"]
            if isinstance(opened_until, (int, float)) and opened_until > now:
                return True
            if opened_until is not None and opened_until <= now:
                state["opened_until"] = None
                state["consecutive_failures"] = 0
            return False

    def record_success(self, provider_name: str) -> None:
        with self._lock:
            state = self._state[provider_name]
            state["consecutive_failures"] = 0
            state["opened_until"] = None

    def record_failure(
        self,
        provider_name: str,
        *,
        threshold: int,
        open_seconds: int,
    ) -> bool:
        with self._lock:
            state = self._state[provider_name]
            state["consecutive_failures"] = int(state["consecutive_failures"]) + 1
            if int(state["consecutive_failures"]) >= threshold:
                state["opened_until"] = self._clock() + open_seconds
                state["consecutive_failures"] = 0
                return True
            return False

    def snapshot(self) -> dict[str, CircuitStateSnapshot]:
        now = self._clock()
        with self._lock:
            snapshot: dict[str, CircuitStateSnapshot] = {}
            for provider_name, state in self._state.items():
                opened_until = state["opened_until"]
                is_open = isinstance(opened_until, (int, float)) and opened_until > now
                snapshot[provider_name] = CircuitStateSnapshot(
                    state="open" if is_open else "closed",
                    opened_until=float(opened_until) if is_open else None,
                    consecutive_failures=int(state["consecutive_failures"]),
                )
            return snapshot

    def reset(self) -> None:
        with self._lock:
            self._state.clear()


class OperationalMetricsStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._request_counts: Counter[str] = Counter(total=0)
        self._provider_success: Counter[str] = Counter()
        self._provider_transport_errors: Counter[str] = Counter()
        self._provider_schema_errors: Counter[str] = Counter()
        self._provider_generic_errors: Counter[str] = Counter()
        self._provider_circuit_open: Counter[str] = Counter()
        self._fallbacks: Counter[str] = Counter()
        self._redactions: Counter[str] = Counter()
        self._rate_limit_hits = 0

    def record_request_started(self) -> None:
        with self._lock:
            self._request_counts["total"] += 1

    def record_request_outcome(self, status_label: str) -> None:
        with self._lock:
            self._request_counts[status_label] += 1

    def record_rate_limit_hit(self) -> None:
        with self._lock:
            self._rate_limit_hits += 1

    def record_provider_success(self, provider_name: str) -> None:
        with self._lock:
            self._provider_success[provider_name] += 1

    def record_provider_transport_error(self, provider_name: str) -> None:
        with self._lock:
            self._provider_transport_errors[provider_name] += 1

    def record_provider_schema_error(self, provider_name: str) -> None:
        with self._lock:
            self._provider_schema_errors[provider_name] += 1

    def record_provider_generic_error(self, provider_name: str) -> None:
        with self._lock:
            self._provider_generic_errors[provider_name] += 1

    def record_provider_circuit_open(self, provider_name: str) -> None:
        with self._lock:
            self._provider_circuit_open[provider_name] += 1

    def record_fallback(self, reason: str) -> None:
        with self._lock:
            self._fallbacks[reason] += 1

    def record_redactions(self, counts: dict[str, int]) -> None:
        with self._lock:
            self._redactions.update(counts)

    def snapshot(self, *, circuit_breakers: dict[str, CircuitStateSnapshot]) -> dict[str, Any]:
        with self._lock:
            return {
                "providers": {
                    "success": dict(self._provider_success),
                    "transport_errors": dict(self._provider_transport_errors),
                    "schema_errors": dict(self._provider_schema_errors),
                    "generic_errors": dict(self._provider_generic_errors),
                    "circuit_open_skips": dict(self._provider_circuit_open),
                },
                "circuit_breakers": {
                    provider_name: {
                        "state": circuit.state,
                        "opened_until": circuit.opened_until,
                        "consecutive_failures": circuit.consecutive_failures,
                    }
                    for provider_name, circuit in circuit_breakers.items()
                },
                "requests": dict(self._request_counts),
                "fallbacks": dict(self._fallbacks),
                "redactions": dict(self._redactions),
                "rate_limits": {"hits": self._rate_limit_hits},
            }

    def reset(self) -> None:
        with self._lock:
            self._request_counts.clear()
            self._request_counts["total"] = 0
            self._provider_success.clear()
            self._provider_transport_errors.clear()
            self._provider_schema_errors.clear()
            self._provider_generic_errors.clear()
            self._provider_circuit_open.clear()
            self._fallbacks.clear()
            self._redactions.clear()
            self._rate_limit_hits = 0


class InMemoryAuditTrailStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: deque[dict[str, Any]] = deque()

    def record_event(self, event: dict[str, Any], *, max_events: int, maxlen: int) -> None:
        sanitized_event = sanitize_technical_payload(event, maxlen=maxlen)
        with self._lock:
            while len(self._events) >= max_events:
                self._events.popleft()
            self._events.append(sanitized_event)

    def snapshot(self, *, retention_mode: str) -> dict[str, Any]:
        with self._lock:
            events = list(self._events)
        return {
            "events": events,
            "count": len(events),
            "retention_mode": retention_mode,
        }

    def reset(self) -> None:
        with self._lock:
            self._events.clear()


analyze_rate_limiter = InMemoryRateLimiter()
provider_circuit_breakers = InMemoryCircuitBreakerRegistry()
operational_metrics = OperationalMetricsStore()
audit_trail = InMemoryAuditTrailStore()


def sanitize_technical_payload(value: object, *, maxlen: int) -> object:
    if value is None or isinstance(value, bool | int | float):
        return value
    if isinstance(value, str):
        return value[:maxlen]
    if isinstance(value, dict):
        return {
            str(key)[:maxlen]: sanitize_technical_payload(item, maxlen=maxlen)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [sanitize_technical_payload(item, maxlen=maxlen) for item in value]
    return str(value)[:maxlen]


def build_log_event(event_name: str, **fields: object) -> str:
    maxlen = get_settings().audit_event_maxlen
    payload = sanitize_technical_payload({"event": event_name, **fields}, maxlen=maxlen)
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def log_analysis_event(event_name: str = "analysis_request", **fields: object) -> None:
    logger.info(build_log_event(event_name, **fields))


def derive_fallback_reason(provider: str) -> str | None:
    if not provider.startswith("fallback:"):
        return None
    _, _, reason = provider.partition(":")
    return reason or None


def resolve_request_id(value: str | None) -> str:
    maxlen = get_settings().audit_event_maxlen
    if value is None:
        from uuid import uuid4

        return uuid4().hex
    stripped = value.strip()
    if not stripped:
        from uuid import uuid4

        return uuid4().hex
    sanitized = sanitize_technical_payload(stripped, maxlen=maxlen)
    return str(sanitized)


def reset_security_state() -> None:
    analyze_rate_limiter.reset()
    provider_circuit_breakers.reset()
    operational_metrics.reset()
    audit_trail.reset()
