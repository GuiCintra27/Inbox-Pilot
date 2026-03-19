# Phase 02 — Backend contract and ingestion

## Objetivo

Entregar a API de análise com contrato estável, ingestão de texto e arquivos e respostas de erro previsíveis.

## Escopo incluído

- implementar `POST /analyze`
- aceitar `email_text`
- aceitar `email_file`
- suportar `.txt`
- suportar `.pdf`
- extrair e normalizar texto
- devolver payload final no formato fechado
- padronizar erros
- escrever testes do backend

## Fora de escopo

- integração com OpenAI
- fallback heurístico final
- polish de UI
- deploy de produção

## Dependências de entrada

- Fase 1 concluída
- app FastAPI e config de ambiente já existentes

## Entregáveis

- endpoint `POST /analyze`
- schemas Pydantic para resposta
- extractors de `.txt` e `.pdf`
- normalização básica de texto
- mensagens de erro claras
- suíte de testes de unidade e integração do backend

## Checklist de implementação

- definir schema de resposta do endpoint
- definir regra mínima para entrada sem texto/arquivo
- implementar parsing de texto livre
- implementar extractor de `.txt`
- implementar extractor de `.pdf`
- normalizar espaços e ruído básico do conteúdo
- padronizar códigos HTTP de erro
- retornar payload com:
  - `category`
  - `confidence`
  - `rationale`
  - `suggested_reply`
  - `keywords`
  - `provider`
- criar testes para texto válido
- criar testes para `.txt` válido
- criar testes para `.pdf` válido
- criar testes para entrada inválida
- criar testes para falha de parsing

## Critérios de aceite

- `POST /analyze` aceita texto
- `POST /analyze` aceita `.txt`
- `POST /analyze` aceita `.pdf`
- payload segue exatamente o contrato global
- erros previsíveis retornam resposta útil e status coerente
- testes cobrem caminhos feliz e principais falhas

## Riscos

- ambiguidade sobre precedência quando texto e arquivo forem enviados juntos
- PDFs com extração ruim
- payload instável antes da Fase 3 começar

## Ownership por subagent

### Subagent A — API layer

Responsável por:
- schemas
- validação
- handlers HTTP
- mapeamento de erros

Não pode alterar:
- contratos do frontend
- pipeline de CI/CD
- heurísticas de AI/fallback

### Subagent B — Ingestion layer

Responsável por:
- extractors `.txt` e `.pdf`
- normalização
- utilitários de linguagem

Não pode alterar:
- UI
- workflows do GitHub
- shape do payload sem alinhamento com Subagent A

### Subagent C — Backend QA and contract docs

Responsável por:
- testes do backend
- casos inválidos
- documentação do contrato técnico interno

Não pode alterar:
- lógica de UI
- configuração de release
- comportamento dos extractors sem necessidade de correção de teste
