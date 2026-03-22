# Security P1 Plan

Plano operacional da segunda onda de hardening do backend do Inbox Pilot.

## Objetivo

Aumentar a proteção da camada de IA sem mudar o contrato público do produto, adicionando redaction pragmática, resiliência por provider e visibilidade operacional interna.

## Defaults fechados

- `REDACTION_ENABLED=true`
- `PROVIDER_TIMEOUT_SECONDS=12`
- `PROVIDER_RETRY_ATTEMPTS=1`
- `PROVIDER_RETRY_BACKOFF_MS=250`
- `CIRCUIT_BREAKER_FAILURE_THRESHOLD=3`
- `CIRCUIT_BREAKER_OPEN_SECONDS=120`

## Escopo fechado

- redaction balanceada antes de providers externos
- retry curto para falhas de transporte
- circuit breaker em memória por provider
- métricas operacionais em memória
- endpoint técnico `GET /ops/llm-health`

## Política de redaction

Tokens estáveis:

- email -> `[EMAIL]`
- telefone -> `[PHONE]`
- CPF -> `[CPF]`
- CNPJ -> `[CNPJ]`
- IDs operacionais contextualizados -> `[OP_ID]`

Rótulos aceitos para `OP_ID`:

- `pedido`
- `order`
- `invoice`
- `fatura`
- `ticket`
- `chamado`
- `protocolo`
- `ref`
- `referência`
- `nota fiscal`

O fallback local continua usando o texto normalizado original.

## Política de resiliência

- retry apenas para falha de transporte/timeout
- sem retry para resposta inválida de schema
- abrir circuito após 3 falhas consecutivas por provider
- circuito aberto por 120 segundos
- provider sem chave não conta como falha

## Endpoint interno

- `GET /ops/llm-health`
- retorno inclui:
  - `providers`
  - `circuit_breakers`
  - `requests`
  - `fallbacks`
  - `redactions`
  - `rate_limits`

## Fora de escopo

- autenticação do endpoint interno
- PII redaction avançada com NLP
- circuit breaker distribuído
- métricas via Prometheus
- política formal de retenção e privacidade
