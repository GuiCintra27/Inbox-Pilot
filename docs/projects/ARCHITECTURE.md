# Arquitetura

## Visão geral

A solução é dividida em duas aplicações com responsabilidades bem definidas:

- Frontend em Next.js para experiência do usuário e apresentação da demo
- Backend em FastAPI para ingestão, parsing, classificação e geração de resposta

Essa separação permite elevar a qualidade visual do produto sem comprometer a clareza do backend e mantém o contrato da solução concentrado em uma API pequena.

## Mapa de camadas

| Camada | Diretório principal | Responsabilidade |
| --- | --- | --- |
| App web | `frontend/src/app` | shell do App Router, landing page e composição das seções |
| Componentes de interface | `frontend/src/components` | formulário, painel de resultado, cards e blocos visuais da demo |
| Cliente HTTP | `frontend/src/lib` | chamada da API e normalização das mensagens de erro |
| API | `backend/src/app/api` | endpoints HTTP, validação de entrada e resposta |
| Serviços | `backend/src/app/services` | ingestão, parsing, NLP, análise, fallback e orquestração |
| Núcleo | `backend/src/app/core` | settings, segurança, redaction, NLP clássico e utilidades técnicas |
| Domínio | `backend/src/app/domain` | contratos internos e estruturas do fluxo de análise |

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
- aplicar pré-processamento NLP clássico
- classificar o email
- sugerir uma resposta automática
- retornar payload simples para consumo do frontend

Stack-alvo:

- FastAPI
- serviços internos para parsing e classificação
- integração com provedores de AI
- fallback heurístico local

## Fluxo principal

1. O usuário envia texto ou arquivo pelo frontend.
2. O frontend envia `multipart/form-data` para `POST /analyze`.
3. O backend extrai e normaliza o conteúdo.
4. O backend gera artefatos de NLP: idioma, tokens, stopwords removidas e stems.
5. O backend redige padrões sensíveis antes de chamar providers externos.
6. O backend tenta Gemini, depois OpenRouter e por fim fallback local.
7. O backend valida o schema de saída e devolve o payload final.
8. O frontend exibe categoria, confiança, justificativa, provider e resposta sugerida.

## Pipeline NLP

O projeto implementa uma camada explícita de NLP clássica antes da análise principal:

- normalização textual
- detecção de idioma
- tokenização
- remoção de stopwords em português e inglês
- stemming com Snowball

Essa camada não substitui o provider de AI. Ela serve para:

- cumprir o requisito de pré-processamento do desafio
- apoiar o fallback heurístico
- padronizar o texto antes da classificação

## Orquestração de AI

Estratégia atual:

- Gemini como provider principal
- OpenRouter como fallback externo
- fallback local resiliente como último nível

Controles de robustez:

- validação de formato da resposta
- rate limit no endpoint de análise
- circuit breaker por provider
- retry curto para falhas de transporte
- redaction antes dos providers externos

## Integração

O frontend consome um único contrato principal do backend:

- `GET /health`
- `POST /analyze`

E, para operação técnica:

- `GET /ops/llm-health`
- `GET /ops/audit-trail`

## Deploy

- Frontend na Vercel
- Backend no Render
- Comunicação por URL pública configurada no frontend

## Entrega contínua

- Repositório central no GitHub
- CI via GitHub Actions para validar frontend e backend
- Preview deploy do frontend em pull requests
- Deploy contínuo da branch principal para os ambientes publicados
- Releases versionadas para registrar evolução do produto

## Guardrails e observabilidade

- `X-Request-ID` por request para rastreabilidade
- zero content retention por padrão
- audit trail técnico em memória
- endpoints `/ops/*` protegidos por ambiente e token fora de `local`
- smoke fixtures para texto, upload e prompt injection

## Decisões de escopo

- Sem autenticação no escopo atual
- Sem banco de dados no escopo atual
- Sem fila assíncrona no escopo atual
- Sem fine-tuning de modelo no escopo atual
- Foco em demo forte, fluxo simples e boa explicação técnica
