# Inbox Pilot

Inbox Pilot é uma solução para automatizar a triagem de emails operacionais, classificando mensagens em `Produtivo` ou `Improdutivo` e sugerindo uma resposta automática coerente com o contexto.

## Direção do projeto

- Frontend em Next.js com foco em experiência visual forte para demo
- Backend em FastAPI para upload, parsing e classificação
- Deploy separado: Vercel no frontend e Render no backend
- Integração com Gemini como provider principal, OpenRouter como fallback externo e fallback local resiliente
- Fluxo de CI/CD no GitHub com releases versionadas

## Objetivo do produto

Inbox Pilot está pronto para apresentação: o fluxo principal funciona de ponta a ponta, o CI/CD está ativo, o deploy-alvo está documentado e a narrativa pública foi ajustada para mostrar um produto final, não um protótipo técnico.

## Documentação principal

- [Índice público do projeto](./docs/projects/INDEX.md)
- [Visão do produto](./docs/projects/PRODUCT-OVERVIEW.md)
- [Fluxo do usuário](./docs/projects/USER-FLOW.md)
- [Arquitetura](./docs/projects/ARCHITECTURE.md)
- [Referência técnica](./docs/projects/TECHNICAL-REFERENCE.md)
- [Deploy](./docs/projects/DEPLOYMENT.md)
- [CI/CD e releases](./docs/projects/CI-CD-RELEASES.md)
- [`render.yaml`](./render.yaml) para o backend no Render

## Documentação interna

- [Notas locais de trabalho](./docs/local/README.md)

## Operação local

Estrutura ativa do monorepo:

- `frontend/` para o app Next.js
- `backend/` para a API FastAPI
- `.github/workflows/` para CI e releases

Primeira execução:

```bash
make setup
```

Esse comando:

- cria `.venv/` na raiz do projeto
- instala as dependências do frontend
- instala as dependências do backend dentro da virtualenv
- cria `frontend/.env.local` e `backend/.env` a partir dos exemplos, se ainda não existirem

Se você já tinha rodado uma versão anterior do setup e quiser recriar os arquivos locais de ambiente:

```bash
make env-reset
```

Para subir a aplicação:

Terminal 1:

```bash
make backend-dev
```

Terminal 2:

```bash
make frontend-dev
```

O target do frontend agora:

- fixa a porta `3000` por padrão
- falha com mensagem clara se a porta já estiver ocupada
- limpa automaticamente o cache `.next` se ele tiver sido gerado a partir de outro caminho absoluto do projeto

Se você quiser forçar uma limpeza manual do cache do Next:

```bash
make frontend-reset
```

URLs locais:

- frontend: `http://localhost:3000`
- backend: `http://localhost:8000`
- health check: `http://localhost:8000/health`

Comandos úteis:

```bash
make setup
make env-init
make env-reset

make frontend-install
make frontend-dev
make frontend-reset
make frontend-lint
make frontend-typecheck
make frontend-build

make backend-install
make backend-dev
make backend-lint
make backend-test
```

## Deploy

- Vercel deve apontar para `frontend/` como root directory
- Render pode usar [`render.yaml`](./render.yaml) como baseline do backend, com secrets e política de auto-deploy ajustados no painel
- `NEXT_PUBLIC_API_BASE_URL` precisa apontar para a URL pública do backend publicado
- `ALLOWED_ORIGINS` no backend de produção deve incluir apenas os domínios públicos do frontend

## Status

- Fluxo principal do produto implementado em frontend e backend
- Análise com Gemini, OpenRouter e fallback local resiliente
- Hardening de segurança concluído em P0, P1 e P2
- CI em PR e push para `main`
- Deploy-alvo documentado para Vercel e Render
- Releases semânticas e changelog ancorados em `release-please`
- Smoke final validado com texto, upload `.txt` e entrada inválida

## Prontidão de lançamento

- Interface pronta para demonstração pública
- Contrato da API estável entre frontend e backend
- Endpoints operacionais internos protegidos por ambiente e token
- Documentação operacional e técnica alinhada ao estado real do produto
