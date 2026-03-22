# Security P2 Plan

Plano operacional da terceira onda de hardening do backend do Inbox Pilot.

## Objetivo

Fechar a lacuna restante de privacy + audit hardening sem mudar o contrato público do produto, adotando zero retention de conteúdo operacional e uma trilha técnica curta em memória por request.

## Defaults fechados

- `ZERO_CONTENT_RETENTION=true`
- `AUDIT_TRACE_ENABLED=true`
- `AUDIT_RECENT_EVENTS_LIMIT=200`
- `AUDIT_EVENT_MAXLEN=120`
- `AUDIT_REQUEST_ID_HEADER=X-Request-ID`

## Escopo fechado

- zero retention de conteúdo operacional
- `request_id` consistente em todo `POST /analyze`
- trilha técnica resumida por request
- buffer circular em memória com eventos recentes
- endpoint técnico `GET /ops/audit-trail`

## Política de retenção

Nunca reter deliberadamente:

- corpo bruto do email
- texto extraído do arquivo
- texto redigido enviado ao provider
- `suggested_reply`
- `rationale`
- `keywords`
- nome completo do arquivo

Permitir apenas:

- métricas agregadas
- logs técnicos truncados
- eventos técnicos resumidos em memória

## Campos permitidos em audit/log

- `request_id`
- `timestamp`
- `status`
- `source`
- `file_type`
- `input_chars`
- `provider_attempts`
- `final_provider`
- `fallback_reason`
- `redaction_summary`
- `duration_ms`

## Campos proibidos em audit/log

- `email_text`
- texto extraído
- texto redigido
- `suggested_reply`
- `rationale`
- `keywords`
- nome completo do arquivo

## Endpoint interno

- `GET /ops/audit-trail`
- retorno inclui:
  - `events`
  - `count`
  - `retention_mode`

## Fora de escopo

- autenticação do endpoint interno
- retenção em banco, Redis ou arquivo
- observabilidade externa/SIEM
- políticas por tenant
- export persistente de trilha de auditoria
