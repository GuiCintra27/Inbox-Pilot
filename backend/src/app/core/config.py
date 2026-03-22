import json
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Inbox Pilot Backend"
    app_env: str = "local"
    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
            "http://localhost:3002",
            "http://127.0.0.1:3002",
        ]
    )
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    openrouter_api_key: str = ""
    openrouter_model: str = "google/gemini-2.0-flash-001"
    max_email_text_chars: int = 12_000
    max_upload_bytes: int = 1_048_576
    max_pdf_pages: int = 10
    max_provider_input_chars: int = 8_000
    rate_limit_analyze_requests: int = 20
    rate_limit_window_seconds: int = 60
    provider_timeout_seconds: float = 12
    provider_retry_attempts: int = 1
    provider_retry_backoff_ms: int = 250
    circuit_breaker_failure_threshold: int = 3
    circuit_breaker_open_seconds: int = 120
    redaction_enabled: bool = True
    zero_content_retention: bool = True
    audit_trace_enabled: bool = True
    audit_recent_events_limit: int = 200
    audit_event_maxlen: int = 120
    audit_request_id_header: str = "X-Request-ID"
    ops_endpoints_enabled: bool = True
    ops_auth_header: str = "X-Ops-Token"
    ops_access_token: str = ""

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: object) -> object:
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                try:
                    parsed = json.loads(stripped)
                except json.JSONDecodeError:
                    parsed = None
                if isinstance(parsed, list):
                    return [str(origin).strip() for origin in parsed if str(origin).strip()]
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
