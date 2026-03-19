# Roadmap de implementação

Este roadmap organiza a execução do produto em fases fechadas, com dependências, status e critérios mínimos para avanço.

## Direção geral

- Estrutura: monorepo com `frontend/`, `backend/`, `docs/`, `.github/`
- Frontend: Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui
- Backend: FastAPI
- Integração: browser envia `multipart/form-data` diretamente para o backend
- AI: OpenAI como caminho principal com fallback local simples
- Entrega: GitHub Actions, Vercel, Render, `release-please`, SemVer

## Contrato global que não deve mudar sem revisão explícita

- `GET /health`
- `POST /analyze`
- entrada: `email_text`, `email_file`
- saída:
  - `category`
  - `confidence`
  - `rationale`
  - `suggested_reply`
  - `keywords`
  - `provider`

## Ordem de execução

### Fase 1 — Foundation

Status: `completed`

Objetivo:
- levantar a fundação do monorepo, congelar convenções e preparar CI/release

Dependências:
- nenhuma

Próxima condição para avançar:
- frontend e backend inicializando localmente
- pipeline básica rodando em PR

Documento detalhado:
- `docs/local/phases/phase-01-foundation.md`

### Fase 2 — Backend contract and ingestion

Status: `completed`

Objetivo:
- implementar a API de análise com parsing de texto, `.txt` e `.pdf`

Dependências:
- Fase 1 concluída

Próxima condição para avançar:
- `POST /analyze` funcional com payload estável

Documento detalhado:
- `docs/local/phases/phase-02-backend-contract-and-ingestion.md`

### Fase 3 — Frontend demo

Status: `planned`

Objetivo:
- construir a jornada principal da demo em Next.js consumindo o backend real

Dependências:
- Fase 1 concluída
- Contrato da Fase 2 estabilizado

Próxima condição para avançar:
- fluxo principal funcionando de ponta a ponta em ambiente local

Documento detalhado:
- `docs/local/phases/phase-03-frontend-demo.md`

### Fase 4 — AI and fallback

Status: `planned`

Objetivo:
- integrar OpenAI e garantir fallback local resiliente

Dependências:
- Fase 2 concluída

Próxima condição para avançar:
- API funcional com e sem chave externa

Documento detalhado:
- `docs/local/phases/phase-04-ai-and-fallback.md`

### Fase 5 — CI/CD and releases

Status: `planned`

Objetivo:
- automatizar checks, deploys e versionamento operacional

Dependências:
- Fase 1 concluída
- Fases 2 e 3 suficientemente estáveis para build/test

Próxima condição para avançar:
- preview, deploy e release funcionando

Documento detalhado:
- `docs/local/phases/phase-05-cicd-and-releases.md`

### Fase 6 — Polish and launch readiness

Status: `planned`

Objetivo:
- fechar qualidade de demo, smoke tests e material de lançamento

Dependências:
- Fases 2, 3, 4 e 5 concluídas

Próxima condição para encerrar:
- frontend publicado consumindo backend publicado com narrativa final pronta

Documento detalhado:
- `docs/local/phases/phase-06-polish-and-launch-readiness.md`

## Regras de avanço entre fases

- Não iniciar a próxima fase como fase principal sem fechar os critérios de aceite da anterior.
- Documentação pode evoluir em paralelo, desde que não reabra decisões já fechadas.
- Subagents só podem trabalhar em paralelo quando o ownership não se sobrepõe.
- Qualquer alteração no contrato global deve ser refletida primeiro neste roadmap e no documento da fase impactada.

## Checklist global de aceite do projeto

- `GET /health` responde corretamente
- `POST /analyze` aceita texto
- `POST /analyze` aceita `.txt`
- `POST /analyze` aceita `.pdf`
- frontend cobre loading, erro e sucesso
- integração real entre frontend publicado e backend publicado
- CI verde em PR
- release gerável pela pipeline
- demo pronta para gravação
