# Security P0 Plan

Plano operacional da primeira onda de hardening do backend do Inbox Pilot.

## Objetivo

Elevar a superfície do `POST /analyze` para um baseline mais forte de segurança sem mudar o contrato público da API nem reabrir a arquitetura do produto.

## Escopo fechado

- limites de texto, upload e PDF
- validação de tipo de arquivo com mismatch explícito
- truncation antes de providers externos
- prompt base com proteção inicial contra prompt injection
- rate limiting em memória por IP
- logging estruturado sem conteúdo sensível

## Defaults do P0

- `MAX_EMAIL_TEXT_CHARS=12000`
- `MAX_UPLOAD_BYTES=1048576`
- `MAX_PDF_PAGES=10`
- `MAX_PROVIDER_INPUT_CHARS=8000`
- `RATE_LIMIT_ANALYZE_REQUESTS=20`
- `RATE_LIMIT_WINDOW_SECONDS=60`

## Comportamentos esperados

### API pública

- `GET /health` permanece inalterado
- `POST /analyze` mantém o mesmo payload de entrada e saída

### Novos códigos HTTP esperados

- `400` para input vazio ou arquivo ilegível
- `413` para texto, arquivo ou PDF acima do limite
- `415` para tipo de arquivo inválido ou mismatch entre extensão e conteúdo
- `429` para excesso de requests no `POST /analyze`

## Logging

Campos mínimos permitidos:

- `request_id`
- `source`
- `file_type`
- `input_chars`
- `provider`
- `status`
- `fallback_reason`
- `duration_ms`

Campos proibidos no log:

- `email_text`
- texto extraído do arquivo
- `suggested_reply`
- nome completo do arquivo

## Fora de escopo

- redaction de PII
- métricas detalhadas
- circuit breaker completo
- rate limiting distribuído
- mudanças no frontend além de compatibilidade com erros já existentes
