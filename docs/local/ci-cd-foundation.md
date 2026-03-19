# CI/CD da Fase 1

Este documento resume a fundação de entrega contínua criada na Fase 1.

## O que ficou preparado

- workflow de CI em `.github/workflows/ci.yml`
- workflow de `release-please` em `.github/workflows/release-please.yml`
- configuração inicial de versionamento semântico
- base para Conventional Commits

## Premissas

- o frontend será validado dentro de `frontend/`
- o backend será validado dentro de `backend/`
- a pipeline principal roda em PR
- releases serão geradas a partir da branch `main`

## Convenção de commits

Uso esperado:

- `feat:` para funcionalidade
- `fix:` para correção
- `docs:` para documentação
- `chore:` para tarefas de manutenção
- `refactor:` para mudanças sem impacto funcional

## Observações

- Os jobs de CI foram preparados para conviver com o bootstrap incremental do monorepo
- Quando `frontend/` e `backend/` existirem, os checks passam a validar lint, testes e build
- A documentação pública de releases continua em `docs/projects/CI-CD-RELEASES.md`

