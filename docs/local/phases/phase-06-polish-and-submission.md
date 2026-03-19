# Phase 06 — Polish and submission

## Objetivo

Fechar o case para submissão com estabilidade mínima, narrativa forte e qualidade visual/operacional suficiente para gravação e avaliação externa.

## Escopo incluído

- revisão visual final
- revisão de copies
- smoke tests end-to-end
- verificação de responsividade
- revisão de acessibilidade básica
- alinhamento final da documentação
- checklist do vídeo
- checklist de submissão

## Fora de escopo

- novas features grandes
- refatorações arquiteturais profundas
- ampliação de escopo do produto

## Dependências de entrada

- Fases 2, 3, 4 e 5 concluídas

## Entregáveis

- frontend e backend publicados funcionando juntos
- documentação final coerente
- checklist de vídeo
- checklist de formulário de submissão
- lista curta de smoke tests aprovados

## Checklist de implementação

- revisar consistência visual da homepage e da tela de resultado
- revisar textos e feedbacks
- validar fluxo real do início ao fim
- validar comportamento mobile
- validar erros mais prováveis
- alinhar README ao estado final
- preparar roteiro curto do vídeo
- preparar checklist do que enviar no formulário

## Critérios de aceite

- frontend publicado consome backend publicado
- fluxo principal funciona de ponta a ponta
- demo está pronta para gravação
- documentação pública, técnica e interna contam a mesma história
- repositório está limpo e navegável

## Riscos

- querer introduzir feature nova na reta final
- docs divergirem da implementação real
- pequenos bugs visuais comprometerem a percepção da demo

## Ownership por subagent

### Subagent A — Visual polish

Responsável por:
- refinamento visual
- consistência entre estados
- ajustes de responsividade

Não pode alterar:
- contratos da API
- pipeline de releases
- arquitetura base das aplicações

### Subagent B — Stability and smoke

Responsável por:
- smoke tests
- correções de integração
- checagem de estabilidade do fluxo principal

Não pode alterar:
- direção visual base sem alinhamento
- escopo funcional principal
- estratégia de deployment

### Subagent C — Submission assets

Responsável por:
- documentação final
- checklist de submissão
- roteiro de demo

Não pode alterar:
- lógica da aplicação
- contratos públicos sem alinhamento explícito
- pipeline técnica além do necessário para documentação
