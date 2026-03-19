# Referência técnica

## Stack-alvo

- Frontend: Next.js com App Router
- Backend: FastAPI
- Parsing de arquivo: `.txt` e `.pdf`
- Engine de análise:
  - Gemini como provedor principal
  - OpenRouter como fallback externo
  - fallback local resiliente para degradação controlada
- Deploy: Vercel + Render
- Entrega: GitHub Actions + releases semânticas

## Endpoints esperados

- `GET /health`
- `POST /analyze`

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

## Responsabilidades por camada

### Frontend

- montar a experiência da demo
- enviar a entrada para o backend
- tratar loading, erro e sucesso
- exibir o resultado de forma clara

### Backend

- receber a entrada
- extrair texto do arquivo
- classificar o email
- gerar resposta sugerida
- devolver resposta consistente para a UI

## Referências adicionais

- Visão do produto: `docs/projects/PRODUCT-OVERVIEW.md`
- Fluxo do usuário: `docs/projects/USER-FLOW.md`
- Arquitetura: `docs/projects/ARCHITECTURE.md`
- Deploy: `docs/projects/DEPLOYMENT.md`
- CI/CD e releases: `docs/projects/CI-CD-RELEASES.md`
