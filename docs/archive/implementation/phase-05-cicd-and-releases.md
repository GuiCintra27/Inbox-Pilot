# Phase 05 — CI/CD and releases

## Objetivo

Automatizar validação, preview, deploy e releases para demonstrar maturidade de engenharia e reduzir risco operacional.

## Escopo incluído

- GitHub Actions para front e back
- preview deploy da Vercel
- deploy de produção do frontend
- deploy automático do backend no Render
- configuração de `release-please`
- changelog automatizado
- convenção de tags e versão

## Fora de escopo

- múltiplos ambientes complexos
- canary deploy
- rollback automatizado avançado
- observabilidade profunda

## Dependências de entrada

- Fase 1 concluída
- Fases 2 e 3 estáveis o suficiente para build/test

## Entregáveis

- workflows de lint/test/build
- integração com preview da Vercel
- deploy do Render documentado e acionável
- release semântica configurada
- changelog operacional

## Checklist de implementação

- definir workflow de PR
- definir workflow de branch principal
- validar build do frontend na CI
- validar testes/lint do backend na CI
- conectar preview da Vercel
- documentar variáveis do Render
- configurar `release-please`
- alinhar Conventional Commits
- gerar primeira release de teste quando apropriado

## Critérios de aceite

- PR dispara checks automáticos
- branch principal publica frontend e backend
- release semântica pode ser gerada sem processo manual improvisado
- documentação do pipeline está correta
- changelog e tags ficam claros para consumo humano e automatizado

## Riscos

- pipeline virar custo alto demais para um produto ainda em estágio inicial
- configurar deploy cedo demais com apps ainda instáveis
- versionamento inconsistente por commits sem padrão

## Ownership por subagent

### Subagent A — GitHub Actions

Responsável por:
- workflows
- caching básico
- organização da execução de checks

Não pode alterar:
- lógica de negócio do backend
- componentes de UI
- contrato da API

### Subagent B — Deploy configuration

Responsável por:
- configuração Vercel/Render
- variáveis de ambiente documentadas
- instruções de integração entre serviços

Não pode alterar:
- comportamento da API
- componentes da UI além do necessário para variáveis
- estratégia de release sem alinhamento

### Subagent C — Releases and changelog

Responsável por:
- `release-please`
- changelog
- convenção de release
- documentação de fluxo de versionamento

Não pode alterar:
- telas da aplicação
- lógica dos endpoints
- deploy config além do necessário para versionamento

## Resultado esperado
O fluxo de release fica ancorado em `release-please`, com changelog gerado automaticamente e versionamento SemVer publicado a partir de Conventional Commits.
