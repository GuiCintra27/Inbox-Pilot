# Checklist de apresentação

## Produto

- frontend carregando sem erro visual em desktop
- frontend carregando sem quebra em mobile
- backend respondendo `GET /health`
- `POST /analyze` funcionando com texto livre
- `POST /analyze` funcionando com arquivo `.txt`
- erro de entrada inválida exibido de forma clara

## Deploy

- `NEXT_PUBLIC_API_BASE_URL` apontando para o backend publicado
- `ALLOWED_ORIGINS` incluindo o domínio real do frontend
- projeto da Vercel ligado ao diretório `frontend/`
- serviço do Render usando `render.yaml`

## Narrativa

- README coerente com o estado real do produto
- documentação pública alinhada entre produto, fluxo, técnica e deploy
- demo destacando problema, fluxo e resultado em menos de dois minutos

## Smoke final

- exemplo produtivo retorna categoria correta
- provider aparece no painel de resultado
- resposta sugerida pode ser copiada
- loading e erro aparecem com feedback claro
