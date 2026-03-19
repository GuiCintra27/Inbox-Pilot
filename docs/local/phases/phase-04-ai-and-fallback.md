# Phase 04 — AI and fallback

## Objetivo

Conectar o backend ao provedor de AI principal e garantir resiliência por meio de fallback local simples.

## Escopo incluído

- integração com OpenAI
- prompt estruturado para classificação
- geração de resposta sugerida
- validação do retorno do provedor
- fallback local heurístico
- few-shot examples curtos
- sinalização do `provider` usado

## Fora de escopo

- fine-tuning
- embeddings
- vetorização
- OCR avançado
- histórico de prompts

## Dependências de entrada

- Fase 2 concluída
- contrato de resposta estabilizado

## Entregáveis

- cliente OpenAI no backend
- prompt inicial fechado
- parsing/validação de resposta
- caminho de fallback local
- testes com provedor mockado
- documentação técnica do comportamento com e sem chave

## Checklist de implementação

- criar cliente/config do provedor
- definir prompt para categoria e resposta
- validar saída contra schema
- mapear falha do provedor para fallback
- implementar heurística local mínima
- adicionar few-shot examples pequenos
- preencher `provider` na resposta
- testar fluxo com chave
- testar fluxo sem chave
- testar resposta inválida do provedor

## Critérios de aceite

- com chave válida, backend usa OpenAI
- sem chave, backend continua funcional
- shape do payload é o mesmo nos dois caminhos
- falha externa não derruba a API
- comportamento fica documentado sem ambiguidade

## Provider contract

Valores esperados para `provider` na Fase 4:

- `openai:<model>` para o caminho principal
- `fallback:no-openai-key` quando a chave não estiver disponível
- `fallback:provider-error` quando o provedor externo falhar
- `fallback:invalid-response` quando a resposta externa não puder ser normalizada

## Test strategy

A suíte desta fase valida três níveis:

- caminho OpenAI mockado sem chamada externa real
- caminhos de fallback quando a credencial não existe ou o provedor falha
- degradação controlada quando a resposta do provedor não respeita o contrato

## Riscos

- prompt gerar respostas fora do schema
- fallback produzir resultados muito divergentes
- dependência exagerada do provedor externo

## Ownership por subagent

### Subagent A — OpenAI integration

Responsável por:
- cliente OpenAI
- prompt
- parsing e validação

Não pode alterar:
- UI do frontend
- workflows de release
- extractors de arquivo sem necessidade direta

### Subagent B — Local fallback

Responsável por:
- heurística local
- consistência básica entre categorias
- resiliência do caminho offline

Não pode alterar:
- layout do frontend
- pipeline do GitHub
- shape do payload global

### Subagent C — AI QA and docs

Responsável por:
- testes com mock
- testes sem chave
- documentação técnica da decisão

Não pode alterar:
- design system da UI
- configuração base da aplicação sem necessidade de teste
