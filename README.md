# Inbox Pilot

Inbox Pilot é uma solução para automatizar a triagem de emails operacionais, classificando mensagens em `Produtivo` ou `Improdutivo` e sugerindo uma resposta automática coerente com o contexto.

## Direção do projeto

- Frontend em Next.js com foco em experiência visual forte para demo
- Backend em FastAPI para upload, parsing e classificação
- Deploy separado: Vercel no frontend e Render no backend
- Integração com API de AI para classificação e geração de resposta
- Fluxo de CI/CD no GitHub com releases versionadas

## Objetivo do produto

Inbox Pilot está pronto para apresentação: o fluxo principal funciona de ponta a ponta, o CI/CD está ativo, o deploy-alvo está documentado e a narrativa pública foi ajustada para mostrar um produto final, não um protótipo técnico.

## Documentação principal

- [Índice público do projeto](./docs/projects/INDEX.md)
- [Visão do produto](./docs/projects/PRODUCT-OVERVIEW.md)
- [Fluxo do usuário](./docs/projects/USER-FLOW.md)
- [Arquitetura](./docs/projects/ARCHITECTURE.md)
- [Referência técnica](./docs/projects/TECHNICAL-REFERENCE.md)
- [Deploy](./docs/projects/DEPLOYMENT.md)
- [CI/CD e releases](./docs/projects/CI-CD-RELEASES.md)
- [`render.yaml`](./render.yaml) para o backend no Render

## Documentação interna

- [Notas locais de trabalho](./docs/local/README.md)

## Operação local

Estrutura ativa do monorepo:

- `frontend/` para o app Next.js
- `backend/` para a API FastAPI
- `.github/workflows/` para CI e releases

Comandos úteis:

```bash
make frontend-install
make frontend-dev
make frontend-lint
make frontend-typecheck
make frontend-build

make backend-install
make backend-dev
make backend-lint
make backend-test
```

## Deploy

- Vercel deve apontar para `frontend/` como root directory
- Render deve usar [`render.yaml`](./render.yaml) como blueprint do backend
- `NEXT_PUBLIC_API_BASE_URL` precisa apontar para a URL pública do backend publicado
- `ALLOWED_ORIGINS` no backend precisa incluir o domínio do frontend publicado

## Status

- Fluxo principal do produto implementado em frontend e backend
- Análise com OpenAI e fallback local resiliente
- CI em PR e push para `main`
- Deploy-alvo documentado para Vercel e Render
- Releases semânticas e changelog ancorados em `release-please`
- Smoke final validado com texto, upload `.txt` e entrada inválida

## Prontidão de lançamento

- Interface pronta para demonstração pública
- Contrato da API estável entre frontend e backend
- Documentação operacional e técnica alinhada ao estado real do produto
- Checklist de lançamento mantido em `docs/local/launch-checklist.md`
