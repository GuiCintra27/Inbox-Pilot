# Referência técnica

## Stack-alvo

- Frontend: Next.js com App Router
- Backend: FastAPI
- Parsing de arquivo: `.txt` e `.pdf`
- AI: provedor externo para classificação e resposta sugerida
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
- o backend deverá decidir a precedência de processamento de forma explícita na implementação

## Saída esperada da API

Payload principal:

- `category`
- `confidence`
- `rationale`
- `suggested_reply`
- `keywords`
- `provider`

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
