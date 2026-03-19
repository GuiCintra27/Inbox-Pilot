# Phase 01 — Foundation

## Objetivo

Criar a fundação do monorepo e congelar as convenções técnicas que servirão de base para todas as fases seguintes.

## Escopo incluído

- criar estrutura `frontend/`, `backend/`, `.github/`
- inicializar Next.js com TypeScript, Tailwind e App Router
- inicializar FastAPI com estrutura mínima de aplicação
- expor `GET /health`
- definir scripts padrão de desenvolvimento e validação
- preparar arquivos `.env.example`
- definir lint, format, naming e organização básica
- configurar CI inicial
- preparar estratégia de Conventional Commits e `release-please`

## Fora de escopo

- `POST /analyze`
- parsing de arquivos
- integração com OpenAI
- UI final da demo
- deploy funcional completo em cloud

## Dependências de entrada

- documentação atual em `docs/projects/`
- contrato global definido no roadmap

## Entregáveis

- `frontend/` inicializável localmente
- `backend/` inicializável localmente
- health endpoint funcional
- `.github/workflows/` com pipeline mínima
- configuração inicial de release/versionamento
- README operacional básico do monorepo

## Checklist de implementação

- criar `frontend/` com App Router e TypeScript
- configurar Tailwind
- instalar e configurar `shadcn/ui`
- criar layout base neutro, sem foco ainda em polish
- criar `backend/` com app FastAPI
- organizar backend em módulos iniciais: app, config, api, services
- implementar `GET /health`
- criar `.env.example` para front e back
- definir scripts padrão de lint, test e dev
- adicionar workflow de CI com build/lint do frontend e validação básica do backend
- preparar configuração inicial de `release-please`

## Critérios de aceite

- `frontend/` sobe localmente sem erro
- `backend/` sobe localmente sem erro
- `GET /health` responde
- pipeline roda em PR
- convenções principais estão documentadas
- nenhuma decisão estrutural crítica fica em aberto

## Status de execução

- foundation do `frontend/` criada
- foundation do `backend/` criada
- `GET /health` implementado
- workflow inicial de CI criado
- release/versionamento inicial preparado
- scripts operacionais básicos do monorepo definidos

## Pendências abertas para a Fase 2

- implementar `POST /analyze`
- estabilizar o contrato completo da API
- conectar frontend e backend no fluxo principal

## Riscos

- gerar scaffolds divergentes do padrão final e precisar retrabalhar cedo
- exagerar no setup do frontend e atrasar as próximas fases
- acoplar versionamento a detalhes ainda instáveis

## Ownership por subagent

### Subagent A — Frontend foundation

Responsável por:
- scaffold de `frontend/`
- Tailwind
- shadcn/ui
- layout base
- scripts do frontend

Não pode alterar:
- contrato da API
- configuração do backend
- decisões de release fora do frontend

### Subagent B — Backend foundation

Responsável por:
- scaffold de `backend/`
- health endpoint
- config/env do backend
- estrutura mínima de módulos

Não pode alterar:
- UI do frontend
- pipeline de release
- contrato de resposta além do necessário para `GET /health`

### Subagent C — CI/release foundation

Responsável por:
- `.github/workflows/`
- `release-please`
- documentação operacional interna
- scripts compartilhados do monorepo

Não pode alterar:
- comportamento funcional da API
- componentes da UI
- estrutura interna dos serviços além do necessário para rodar CI
