# CI/CD e releases

## Objetivo

Tratar o fluxo de entrega como parte da qualidade do projeto, garantindo validação automática, deploy previsível e histórico claro de evolução.

## Estratégia

- Repositório central no GitHub
- Pull requests com validações automáticas
- Preview deploy do frontend na Vercel
- Deploy do backend no Render a partir da branch principal
- Releases versionadas para marcar entregas relevantes

## CI

Checks esperados em pull requests:

- frontend: lint, typecheck, testes e build
- backend: lint, testes e validação básica da API
- verificação de consistência entre contratos principais e documentação técnica
- falha de um slice bloqueia merge até a correção

## CD

- Vercel com preview por pull request
- Vercel em produção a partir da branch principal
- Render com deploy automático do backend na branch principal
- variáveis de ambiente de produção devem ser mantidas fora do código-fonte

## Versionamento

Modelo adotado:

- SemVer no formato `vMAJOR.MINOR.PATCH`

Uso prático neste produto:

- `MAJOR`: quebra relevante de arquitetura ou contrato público
- `MINOR`: funcionalidade nova visível na solução
- `PATCH`: correção ou refinamento sem alteração importante de comportamento

## Releases

Direção sugerida:

- adotar Conventional Commits
- gerar changelog automaticamente
- criar releases no GitHub para checkpoints importantes do produto

Ferramenta recomendada:

- `release-please`

Essa combinação ajuda a demonstrar organização, previsibilidade e maturidade de engenharia sem exagerar a complexidade do projeto.

## Fluxo operacional

1. Um pull request dispara CI no GitHub Actions.
2. Se os checks passarem, o merge para `main` fica elegível.
3. Um push em `main` aciona `release-please`.
4. Quando houver alterações relevantes, a ferramenta atualiza `CHANGELOG.md`, cria ou atualiza a pull request de release e publica tags semânticas no formato `vMAJOR.MINOR.PATCH`.
5. Cada release marca um checkpoint público e rastreável da evolução do produto.

## Governança

- Commits devem seguir Conventional Commits para manter o changelog previsível.
- Mudanças de contrato público devem ser tratadas como alteração relevante de versão.
- O fluxo de release deve permanecer simples o suficiente para ser auditado manualmente.
