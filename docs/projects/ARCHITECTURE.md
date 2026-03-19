# Arquitetura

## Visão geral

A solução será dividida em duas aplicações com responsabilidades bem definidas:

- Frontend em Next.js para experiência do usuário e apresentação da demo
- Backend em FastAPI para ingestão, parsing, classificação e geração de resposta

Essa separação permite elevar a qualidade visual do case sem comprometer a clareza do backend.

## Frontend

Responsabilidades principais:

- apresentar a proposta da ferramenta com uma interface forte e polida
- receber texto livre ou arquivo do usuário
- enviar a entrada para o backend
- exibir categoria, justificativa, confiança e resposta sugerida

Stack-alvo:

- Next.js
- TypeScript
- App Router
- camada visual focada em demo e usabilidade

## Backend

Responsabilidades principais:

- receber `multipart/form-data`
- extrair conteúdo textual de `.txt` e `.pdf`
- normalizar a entrada
- classificar o email
- sugerir uma resposta automática
- retornar payload simples para consumo do frontend

Stack-alvo:

- FastAPI
- serviços internos para parsing e classificação
- integração com provedor de AI

## Integração

Fluxo principal:

1. O usuário envia texto ou arquivo pelo frontend.
2. O frontend chama o backend por HTTP.
3. O backend processa o email e monta a análise.
4. O frontend apresenta o resultado em uma tela de retorno clara e visualmente forte.

## Deploy

- Frontend na Vercel
- Backend no Render
- Comunicação por URL pública configurada no frontend

## Entrega contínua

- Repositório central no GitHub
- CI via GitHub Actions para validar frontend e backend
- Preview deploy do frontend em pull requests
- Deploy contínuo da branch principal para os ambientes publicados
- Releases versionadas para registrar evolução do case

## Decisões de escopo

- Sem autenticação na fase inicial
- Sem banco de dados na fase inicial
- Sem fila assíncrona na fase inicial
- Foco em demo forte, fluxo simples e boa explicação técnica
