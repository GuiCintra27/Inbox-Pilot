# Inbox Pilot

Inbox Pilot é o nome do produto deste case técnico: uma solução para automatizar a triagem de emails operacionais, classificando mensagens em `Produtivo` ou `Improdutivo` e sugerindo uma resposta automática coerente com o contexto.

## Direção do projeto

- Frontend em Next.js com foco em experiência visual forte para demo
- Backend em FastAPI para upload, parsing e classificação
- Deploy separado: Vercel no frontend e Render no backend
- Integração com API de AI para classificação e geração de resposta
- Fluxo de CI/CD no GitHub com releases versionadas

## Objetivo desta fase

O repositório está sendo organizado para refletir a arquitetura-alvo do case antes da implementação definitiva.

## Documentação principal

- [Índice público do projeto](./docs/projects/INDEX.md)
- [Visão do produto](./docs/projects/PRODUCT-OVERVIEW.md)
- [Fluxo do usuário](./docs/projects/USER-FLOW.md)
- [Arquitetura](./docs/projects/ARCHITECTURE.md)
- [Referência técnica](./docs/projects/TECHNICAL-REFERENCE.md)
- [Deploy](./docs/projects/DEPLOYMENT.md)
- [CI/CD e releases](./docs/projects/CI-CD-RELEASES.md)

## Documentação interna

- [Notas locais de trabalho](./docs/local/README.md)

## Operação da Fase 1

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

## Status

- Arquitetura e narrativa documental em alinhamento
- Fase 1 estruturada com foundation de frontend, backend e CI/release
- Implementação funcional do produto começa na Fase 2
