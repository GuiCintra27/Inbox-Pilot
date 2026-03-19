# Phase 03 — Frontend demo

## Objetivo

Construir a jornada principal da demo em Next.js consumindo o backend real e apresentando uma experiência clara, forte e responsiva.

## Escopo incluído

- landing principal
- hero com proposta da ferramenta
- formulário de texto
- upload de arquivo
- feedback visual de seleção
- loading state
- error state
- success state
- exibição do resultado
- ação de copiar resposta
- responsividade

## Fora de escopo

- autenticação
- dashboard secundário
- histórico de análises
- animações complexas que não ajudem a demo

## Dependências de entrada

- Fase 1 concluída
- contrato de `POST /analyze` estabilizado na Fase 2
- variável `NEXT_PUBLIC_API_BASE_URL` definida

## Entregáveis

- tela principal pronta para demo
- integração real com backend
- componentes de resultado
- tratamento claro de loading, erro e sucesso
- UI responsiva em desktop e mobile

## Checklist de implementação

- definir direção visual da homepage
- construir hero e seção principal
- construir textarea para email
- construir input/upload de arquivo
- exibir nome do arquivo selecionado
- enviar `multipart/form-data` ao backend
- tratar loading
- tratar erro de forma amigável
- tratar sucesso e exibir:
  - categoria
  - confiança
  - justificativa
  - resposta sugerida
  - palavras-chave
- adicionar botão de copiar resposta
- incluir exemplos prontos para teste
- validar layout em mobile

## Critérios de aceite

- usuário entende a proposta sem ler docs externas
- texto livre funciona
- upload funciona
- resposta do backend aparece corretamente
- UI não parece boilerplate genérico
- experiência mobile não quebra o fluxo

## Riscos

- UI bonita mas pouco clara
- acoplamento excessivo ao payload do backend
- uso desnecessário de bibliotecas pesadas

## Ownership por subagent

### Subagent A — Visual system and layout

Responsável por:
- layout
- hero
- identidade visual
- responsividade

Não pode alterar:
- contrato do backend
- lógica de análise
- workflows do GitHub

### Subagent B — Form and integration

Responsável por:
- formulário
- upload
- integração HTTP
- estados de loading, erro e sucesso

Não pode alterar:
- visual base definido por Subagent A sem alinhamento
- lógica interna do backend
- configuração de release

### Subagent C — Results and accessibility

Responsável por:
- componentes de resultado
- copy UX
- ação de copiar resposta
- refinamentos de acessibilidade

Não pode alterar:
- contrato do endpoint
- pipeline de deploy
- layout estrutural sem alinhamento com Subagent A
