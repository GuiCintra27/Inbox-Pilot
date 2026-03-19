# Objetivo inicial do case

Objetivo atual de trabalho para este projeto:

- Construir um frontend em Next.js com foco claro em uma demo forte, visualmente caprichada e fácil de navegar
- Construir um backend em FastAPI para receber texto ou arquivo, processar o conteúdo do email e retornar a análise
- Classificar emails entre `Produtivo` e `Improdutivo`
- Sugerir uma resposta automática coerente com a categoria identificada
- Preparar a solução para deploy separado: Vercel no frontend e Render no backend
- Estruturar pipeline de CI/CD no GitHub e releases com versionamento para dar previsibilidade de entrega

Decisão de escopo:
- O foco principal é experiência do usuário, clareza do fluxo e consistência da análise
- O fluxo de entrega também deve passar imagem de projeto maduro, com checks automáticos e releases claras
- Complexidades secundárias como autenticação, banco de dados, fila e painel administrativo ficam fora do escopo inicial

Observação:
- Este documento permanece em `docs/local/` porque representa direcionamento interno de execução
- A documentação voltada para leitura externa deve ficar em `docs/projects/`
- O plano faseado detalhado de implementação fica em `docs/local/implementation-roadmap.md` e em `docs/local/phases/`
