# AGENTS.md - Inbox Pilot

README para agentes de código trabalhando neste repositório.

## Visão geral do projeto

Este repositório guarda o Inbox Pilot, uma solução de automação de triagem de emails com frontend em Next.js, backend em FastAPI e operação orientada a produto.

Direção oficial do projeto:

- Frontend em Next.js com App Router
- Backend em FastAPI
- Deploy do frontend na Vercel
- Deploy do backend no Render
- Integração simples via API HTTP
- CI/CD via GitHub Actions
- Releases com versionamento semântico

## Estado atual esperado

Nesta fase, o repositório está sendo reorganizado para refletir a arquitetura-alvo.

- A documentação pública fica em `docs/projects/`
- A documentação interna de trabalho fica em `docs/local/`
- Implementações antigas que descreviam outra stack não devem ser consideradas referência

## Estilo de arquitetura

### Frontend

- Priorizar experiência visual forte para a demo
- Aceitar texto livre e upload de arquivo
- Consumir uma API backend única e simples
- Evitar complexidade desnecessária de estado global

### Backend

- Expor endpoints pequenos e claros
- Centralizar parsing, classificação e geração de resposta em serviços bem separados
- Aceitar `multipart/form-data` com texto e arquivo
- Preparar integração com provedor de AI e fallback local

## Contrato esperado da solução

### Endpoints

- `GET /health`
- `POST /analyze`

### Entrada principal

- `email_text`
- `email_file`

### Saída principal

- `category`
- `confidence`
- `rationale`
- `suggested_reply`
- `keywords`
- `provider`

## Pontos de atenção

- O material em `docs/local/` não é a vitrine principal do produto
- O material em `docs/local/` não é a camada principal de apresentação do produto
- A narrativa pública do projeto deve ficar consistente entre `README.md` e `docs/projects/`
- Não reintroduzir documentação que descreva a stack descartada como solução-alvo
- Priorizar clareza da demo e coerência da arquitetura antes de expandir escopo
- Tratar pipeline de entrega e versionamento como parte do produto, não como detalhe opcional

## Estrutura documental

```text
inbox-pilot/
- docs/projects/   # documentação pública do produto
- docs/local/      # notas internas e planejamento ativo
- docs/archive/    # histórico interno encerrado
- README.md        # resumo executivo da raiz
- AGENTS.md        # guia para agentes de código
```

## Disciplina de documentação

1. Registrar notas de implementação ativa em `docs/local/`.
2. Promover para `docs/projects/` apenas o que fizer sentido como documentação pública.
3. Mover material encerrado para `docs/archive/`.
4. Manter a arquitetura-alvo coerente em toda a documentação.
5. Manter a estratégia de CI/CD e releases coerente com o estágio do projeto.
