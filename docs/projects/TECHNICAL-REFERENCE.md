# Referência técnica

## Stack-alvo

- Frontend: Next.js com App Router
- Backend: FastAPI
- Parsing de arquivo: `.txt` e `.pdf`
- Engine de análise: `rule-based-preview` nesta fase, com provedor externo entrando na fase de AI
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

Nota de contrato:

- `provider` identifica a engine que produziu a análise
- na Fase 2, o valor esperado é um identificador de preview, como `rule-based-preview`
- na Fase 4, esse mesmo campo passa a identificar o provedor de AI ativo

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
