from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.config import get_settings
from app.core.security import audit_trail, operational_metrics, provider_circuit_breakers

LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


def require_ops_access(request: Request) -> None:
    settings = get_settings()
    client_host = _extract_client_host(request)

    if settings.app_env == "local":
        if client_host in LOOPBACK_HOSTS:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Os endpoints operacionais só aceitam acesso local loopback neste ambiente.",
        )

    if not settings.ops_endpoints_enabled or not settings.ops_access_token.strip():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    provided_token = request.headers.get(settings.ops_auth_header)
    if provided_token != settings.ops_access_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso aos endpoints operacionais não autorizado.",
        )


router = APIRouter(prefix="/ops", dependencies=[Depends(require_ops_access)])


@router.get("/llm-health")
async def llm_health() -> dict[str, object]:
    return operational_metrics.snapshot(
        circuit_breakers=provider_circuit_breakers.snapshot(),
    )


@router.get("/audit-trail")
async def audit_trail_snapshot() -> dict[str, object]:
    settings = get_settings()
    retention_mode = (
        "zero_content_retention" if settings.zero_content_retention else "custom_retention"
    )
    return audit_trail.snapshot(retention_mode=retention_mode)


def _extract_client_host(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"
