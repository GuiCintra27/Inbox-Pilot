# Deploy

## Estratégia

A solução será publicada em duas frentes:

- frontend na Vercel
- backend no Render

## Configuração base

- frontend: projeto Vercel apontando para o diretório `frontend/`
- backend: blueprint do Render usando [`render.yaml`](../../render.yaml)
- variáveis do frontend: `NEXT_PUBLIC_API_BASE_URL`
- variáveis do backend: `APP_ENV`, `ALLOWED_ORIGINS`, `GEMINI_API_KEY`, `GEMINI_MODEL`, `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`

## Frontend

Responsabilidades do deploy:

- hospedar a interface principal da demo
- consumir a URL pública do backend
- permitir navegação direta e teste sem configuração local

Configuração esperada:

- root directory no Vercel: `frontend/`
- build command: `npm run build`
- default production URL do backend injetada via `NEXT_PUBLIC_API_BASE_URL`
- preview deploys ativados em pull requests
- o domínio do frontend publicado deve ser inserido em `ALLOWED_ORIGINS` do backend

## Backend

Responsabilidades do deploy:

- expor os endpoints de análise
- processar uploads e texto livre
- integrar com o provedor de AI

Configuração esperada:

- blueprint do Render via [`render.yaml`](../../render.yaml)
- runtime Python apontando para `backend/`
- start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- `ALLOWED_ORIGINS` incluindo o domínio da Vercel e os hosts locais de desenvolvimento
- substituir o placeholder `https://<your-frontend-domain>.vercel.app` pelo domínio real do frontend publicado

## Comunicação entre aplicações

- o frontend deve usar a URL pública do backend por variável de ambiente
- o backend deve aceitar requisições do frontend publicado
- a solução deve ser testável por terceiros sem instalação local

## Resultado esperado

Qualquer stakeholder deve conseguir abrir a URL do frontend, enviar um email e observar a análise completa com mínima fricção.

## Pipeline de entrega

- Pull requests devem acionar validações automáticas no GitHub
- A Vercel deve publicar previews do frontend para revisão
- O Render deve publicar o backend a partir da branch principal
- Releases versionadas devem marcar entregas relevantes do projeto

## Fluxo operacional

1. Abrir PR com frontend e backend alinhados ao contrato já definido.
2. Validar o frontend na Vercel via preview do PR.
3. Validar o backend no Render usando o blueprint da raiz.
4. Promover a branch principal quando CI e revisão estiverem verdes.
5. Registrar releases com versionamento semântico quando houver entrega relevante.

## Versionamento

- `release-please` deve ser o mecanismo padrão para tags e changelog
