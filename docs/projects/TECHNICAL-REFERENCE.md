# Referência técnica

## Stack-alvo

- Frontend: Next.js com App Router
- Backend: FastAPI
- Parsing de arquivo: `.txt` e `.pdf`
- Pré-processamento NLP:
  - normalização textual
  - detecção de idioma
  - remoção de stopwords (`pt-BR` e `en-US`)
  - stemming com Snowball
- Engine de análise:
  - Gemini como provedor principal
  - OpenRouter como fallback externo
  - fallback local resiliente para degradação controlada
- Deploy: Vercel + Render
- Entrega: GitHub Actions + releases semânticas

## Ambientes e URLs

Local:

- frontend: `http://localhost:3000`
- backend: `http://localhost:8000`
- health: `http://localhost:8000/health`

Publicado:

- frontend: `https://inbox-pilot-mocha.vercel.app/`
- backend: `https://inbox-pilot-backend.onrender.com/`
- health: `https://inbox-pilot-backend.onrender.com/health`

## Endpoints esperados

- `GET /health`
- `POST /analyze`
- `GET /ops/llm-health`
- `GET /ops/audit-trail`

## Resumo dos endpoints

### `GET /health`

- usado para smoke checks locais e health check do Render
- não exige autenticação
- não consulta providers externos

### `POST /analyze`

- recebe texto livre, arquivo ou ambos
- extrai e normaliza o conteúdo
- aplica pré-processamento NLP clássico
- tenta Gemini, depois OpenRouter, depois fallback local
- devolve payload único para o frontend

### `GET /ops/llm-health`

- endpoint técnico interno
- expõe métricas agregadas de providers, circuit breaker e fallback
- protegido por ambiente e token fora de `local`

### `GET /ops/audit-trail`

- endpoint técnico interno
- expõe eventos técnicos resumidos em memória
- não retém corpo de email nem resposta sugerida
- protegido por ambiente e token fora de `local`

## Entrada principal da API

Formato:

- `multipart/form-data`

Campos:

- `email_text`
- `email_file`

Regra esperada:

- o usuário poderá enviar texto, arquivo ou ambos
- quando os dois campos vierem juntos, o backend deve priorizar `email_file`
- `email_text` funciona como entrada principal quando não houver arquivo
- se a extração do arquivo falhar, a requisição deve falhar de forma explícita em vez de cair silenciosamente para o texto

Erros esperados:

- ausência de texto e arquivo: requisição inválida
- arquivo em formato não suportado: rejeição clara
- falha na extração do arquivo: rejeição clara

## Matriz de erros operacionais

- `400` para ausência de conteúdo ou arquivo vazio
- `413` para texto, arquivo ou PDF acima dos limites configurados
- `415` para formato de arquivo inválido ou mismatch entre extensão e conteúdo
- `429` para rate limiting no `POST /analyze`
- `500` para falha inesperada de infraestrutura ou erro interno não recuperável

## Saída esperada da API

Payload principal:

- `category`
- `confidence`
- `rationale`
- `suggested_reply`
- `keywords`
- `provider`

## Contrato de provider

O campo `provider` identifica o caminho real que produziu a análise.

Valores documentados:

- `gemini:<model>` quando a chamada principal ao Gemini é bem-sucedida
- `openrouter:<model>` quando a análise usa OpenRouter após ausência/falha do provider principal
- `fallback:no-provider-key` quando não existe credencial para Gemini ou OpenRouter
- `fallback:provider-error` quando os providers externos falham por transporte/disponibilidade
- `fallback:invalid-response` quando os providers externos retornam payload incompatível

Nota de contrato:

- o frontend consome esse campo para rastreabilidade da demo
- a estrutura do payload não muda entre o caminho principal e o fallback

## Comportamento operacional adicional

- `POST /analyze` devolve `X-Request-ID` em todas as respostas
- se o cliente enviar `X-Request-ID`, o backend reutiliza o valor
- os endpoints `GET /ops/llm-health` e `GET /ops/audit-trail` são técnicos e protegidos
- em ambiente `local`, o acesso aos endpoints `/ops/*` é aceito apenas via loopback
- fora de `local`, o acesso aos endpoints `/ops/*` exige token operacional

## Responsabilidades por camada

### Frontend

- montar a experiência da demo
- enviar a entrada para o backend
- tratar loading, erro e sucesso
- exibir o resultado de forma clara

### Backend

- receber a entrada
- extrair texto do arquivo
- aplicar pré-processamento NLP clássico antes da análise
- classificar o email
- gerar resposta sugerida
- devolver resposta consistente para a UI

## Pipeline NLP

Antes da classificação, o backend executa uma etapa explícita de pré-processamento textual:

1. normalização do texto bruto
2. detecção de idioma
3. tokenização
4. remoção de stopwords para `pt-BR` e `en-US`
5. stemming com Snowball

Esses artefatos são usados para:

- enriquecer o fallback heurístico local
- padronizar o texto antes da análise
- demonstrar aderência ao requisito de NLP do desafio

## Orquestração de providers

Ordem de execução:

1. Gemini
2. OpenRouter
3. fallback local

Controles adicionais:

- redaction antes de providers externos
- timeout, retry curto e circuit breaker por provider
- validação de schema da resposta
- request tracing com `X-Request-ID`

## Nota de privacidade operacional

- por padrão, o backend não retém corpo bruto de email após o request
- a camada operacional mantém apenas métricas agregadas e eventos técnicos resumidos

## Comandos de validação

```bash
make backend-lint
make backend-test
make frontend-lint
make frontend-typecheck
make frontend-build
```

## CI/CD

- CI em push e pull request via GitHub Actions
- release semântica com `release-please`
- backend preparado para deploy no Render
- frontend preparado para deploy na Vercel

## Referências adicionais

- Visão do produto: `docs/projects/PRODUCT-OVERVIEW.md`
- Fluxo do usuário: `docs/projects/USER-FLOW.md`
- Arquitetura: `docs/projects/ARCHITECTURE.md`
- Deploy: `docs/projects/DEPLOYMENT.md`
- CI/CD e releases: `docs/projects/CI-CD-RELEASES.md`
