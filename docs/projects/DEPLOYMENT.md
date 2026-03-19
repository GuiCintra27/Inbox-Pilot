# Deploy

## Estratégia

A solução será publicada em duas frentes:

- frontend na Vercel
- backend no Render

## Frontend

Responsabilidades do deploy:

- hospedar a interface principal da demo
- consumir a URL pública do backend
- permitir navegação direta e teste sem configuração local

## Backend

Responsabilidades do deploy:

- expor os endpoints de análise
- processar uploads e texto livre
- integrar com o provedor de AI

## Comunicação entre aplicações

- o frontend deve usar a URL pública do backend por variável de ambiente
- o backend deve aceitar requisições do frontend publicado
- a solução deve ser testável por terceiros sem instalação local

## Resultado esperado

O recruiter ou avaliador deve conseguir abrir a URL do frontend, enviar um email e observar a análise completa com mínima fricção.

## Pipeline de entrega

- Pull requests devem acionar validações automáticas no GitHub
- A Vercel deve publicar previews do frontend para revisão
- O Render deve publicar o backend a partir da branch principal
- Releases versionadas devem marcar entregas relevantes do projeto
