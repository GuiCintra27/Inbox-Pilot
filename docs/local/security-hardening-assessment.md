# Security Hardening Assessment

Diagnóstico interno dos controles de segurança atuais do Inbox Pilot e do que ainda precisa ser implementado para tratar a camada de IA como uma superfície de risco forte, e não apenas funcional.

## Objetivo

Consolidar:

- o que já existe hoje como guardrail útil
- o que ainda está ausente para um nível forte de segurança
- a ordem recomendada de implementação

Este documento substitui o antigo foco em roadmap de fases como principal referência interna ativa.

## Resumo executivo

Status do P0: `Concluído`

Status do P1: `Concluído`

Status do P2: `Em execução com defaults fechados`

Documento operacional desta etapa:

- `docs/local/security-p0-plan.md`
- `docs/local/security-p1-plan.md`
- `docs/local/security-p2-plan.md`

O produto já possui guardrails estruturais importantes:

- contrato de resposta fixo entre backend e frontend
- validação do payload de resposta vindo dos providers
- fallback em cascata entre providers externos e fallback local
- separação entre ingestão, orquestração de análise e fallback
- `ALLOWED_ORIGINS` configurável para CORS

Isso evita quebra de schema, melhora a resiliência e reduz parte do risco operacional.

Ainda assim, o nível atual não pode ser classificado como hardening forte. Os principais gaps concentram-se em:

- controle de entrada
- proteção contra prompt injection
- privacidade de dados enviados aos modelos
- rate limiting e abuso
- observabilidade com redaction
- política explícita de segurança por provider

## Estado atual por categoria

### 1. Contrato e integridade da resposta

Status: `Parcialmente forte`

Já existe:

- shape fixo de saída para `POST /analyze`
- validação do retorno dos providers antes de devolver ao frontend
- fallback quando o provider falha ou responde fora do formato esperado
- campo `provider` explícito para rastreabilidade

Ainda falta:

- limitar explicitamente faixas válidas de `confidence`
- garantir allowlist fechada para `category`
- garantir truncation/size cap de `rationale`, `suggested_reply` e `keywords`
- normalizar sempre strings de saída para evitar payload excessivo

### 2. Segurança de entrada e ingestão

Status: `Fraco`

Já existe:

- aceitação restrita ao fluxo de texto, `.txt` e `.pdf`
- precedência documentada entre texto e arquivo

Ainda falta:

- limite explícito de tamanho do request
- limite explícito de tamanho de arquivo
- limite de páginas para PDF
- validação de MIME real além da extensão
- proteção contra PDFs malformados ou excessivamente pesados
- truncation do texto extraído antes de enviar ao provider
- normalização forte de entrada

### 3. Prompt injection e controle de instruções

Status: `Fraco`

Risco atual:

- o corpo do email é conteúdo não confiável
- o modelo pode receber instruções maliciosas embutidas no próprio email
- não há ainda política documentada de ignorar comandos presentes no input

Ainda falta:

- system prompt com regra explícita: tratar o email apenas como dado, nunca como instrução operacional do modelo
- separação clara entre instruções do sistema e conteúdo do usuário
- negação explícita de override por texto do email
- classificação defensiva para conteúdo que tente manipular o modelo
- testes específicos de prompt injection

### 4. Privacidade e proteção de dados

Status: `Fraco`

Risco atual:

- emails podem conter PII, dados financeiros, nomes, fornecedores, tickets e contexto operacional sensível
- sem redaction, o conteúdo segue bruto para provider externo

Ainda falta:

- redaction de dados sensíveis antes do envio ao LLM quando possível
- política clara sobre quais dados podem sair do sistema
- documentação de retenção e uso por provider
- logs sem conteúdo bruto do email
- separação entre logs operacionais e conteúdo analisado

### 5. Abuso, exposição pública e rate limiting

Status: `Fraco`

Risco atual:

- se o backend for exposto publicamente sem proteção, ele pode ser usado para abuso de custo ou negação de serviço

Ainda falta:

- rate limiting por IP
- limites de concorrência
- proteção mínima para endpoints públicos
- timeouts defensivos para requests de upload
- política de erro consistente sob carga

### 6. Resiliência por provider

Status: `Parcialmente forte`

Já existe:

- estratégia em cascata: Gemini -> OpenRouter -> fallback local
- tratamento de resposta inválida
- tratamento de indisponibilidade do provider

Ainda falta:

- timeout explícito por provider
- retry policy controlada
- circuit breaker simples para evitar insistência em provider degradado
- allowlist formal de domínios externos usados
- logs estruturados por falha de provider

### 7. Observabilidade, auditoria e resposta a incidentes

Status: `Fraco`

Já existe:

- rastreabilidade funcional do provider pelo payload

Ainda falta:

- request id / trace id por análise
- logs estruturados de sucesso/falha
- redaction em logs
- métricas por provider
- métricas de fallback
- alertas para crescimento de falhas ou uso anômalo

### 8. Frontend e superfície de apresentação

Status: `Razoável`

Já existe:

- contrato tipado para consumo do backend
- renderização padrão do React, sem necessidade de HTML arbitrário do usuário

Ainda falta:

- validação mais explícita do lado do cliente antes do upload
- feedback de limite de tamanho/tipo de arquivo
- mensagens de erro mapeadas para cenários de segurança
- não expor nenhum segredo em variáveis `NEXT_PUBLIC_*`

## Lacunas prioritárias

### Prioridade P0

Estas são as mudanças mínimas para poder chamar a solução de fortemente protegida no contexto do produto atual:

1. Limitar tamanho de request, texto e arquivo no backend.
2. Validar MIME real e impor allowlist de tipos aceitos.
3. Adicionar instrução anti-prompt-injection no fluxo de provider.
4. Truncar e normalizar o conteúdo antes de enviar ao modelo.
5. Implementar rate limiting no `POST /analyze`.
6. Garantir logs sem corpo bruto do email.

### Prioridade P1

1. Redaction básica de PII e padrões sensíveis antes do provider externo.
2. Timeout, retry curto e circuit breaker simples por provider.
3. Métricas por provider, fallback e erro.
4. Testes dedicados para prompt injection e oversized inputs.

### Prioridade P2

1. Política formal de retenção e privacidade.
2. Auditoria operacional com trace id.
3. Modo enterprise com políticas por tenant, se o produto evoluir nessa direção.

## Hardening backlog recomendado

### Backend

- adicionar `MAX_EMAIL_TEXT_CHARS`
- adicionar `MAX_UPLOAD_BYTES`
- adicionar `MAX_PDF_PAGES`
- validar MIME/extension e rejeitar mismatch
- truncar texto extraído antes do provider
- aplicar unicode normalization
- rejeitar payload sem conteúdo útil após parsing

### LLM orchestration

- reescrever prompts com regra explícita de não obedecer instruções do email
- tratar corpo do email como dado não confiável
- limitar tamanho máximo da resposta do modelo
- reforçar parsing estrito do JSON
- adicionar testes de jailbreak/prompt injection

### Resilience

- definir timeout de rede por provider
- definir retry curto com backoff mínimo
- registrar motivo de fallback em log estruturado
- bloquear provider temporariamente após sequência de falhas

### Abuse control

- incluir rate limiting
- incluir proteção de burst
- limitar uploads concorrentes
- preparar resposta consistente para 429

### Privacy

- adicionar camada de redaction opcional para CPF, email, telefone, invoice ids e padrões conhecidos
- evitar logging de conteúdo completo
- documentar claramente o envio para providers de terceiros

## O que já é reaproveitável

Mesmo com lacunas de segurança, a arquitetura atual já ajuda bastante:

- service layer separada
- providers desacoplados
- fallback local já existente
- schema fixo já adotado
- frontend já preparado para ler o `provider`

Ou seja: o hardening forte pode ser adicionado sem reabrir a arquitetura.

## Recomendação objetiva

Se o objetivo for elevar o produto para um patamar forte de segurança sem inflar escopo:

1. Implementar primeiro P0 completo.
2. Tratar P1 como segunda onda curta.
3. Só depois revisar privacidade e observabilidade de longo prazo.

## Critério para considerar o produto fortemente protegido

O Inbox Pilot só deve ser tratado internamente como tendo guardrails fortes quando cumprir, no mínimo:

- limite explícito de input e upload
- validação forte de tipo de arquivo
- proteção explícita contra prompt injection
- rate limiting no endpoint público
- logs sem conteúdo sensível bruto
- timeout e fallback robustos por provider
- testes automatizados cobrindo abuso, oversized input e resposta inválida
