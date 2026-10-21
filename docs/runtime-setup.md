# Instalar e executar os agentes

Os seis agentes estão no repositório privado `mullz013/eixo-ai` (branch `eixo/setup-multiagent-v1.1` até merge na `main`).

1. Instale Claude Code, Git e o GitHub CLI no seu computador; autentique `gh auth login`.
2. Clone o `eixo-ai` e instale as seis definições `.claude/agents/*.md` na configuração do Claude Code (por exemplo, no diretório de agentes do usuário, se disponível nessa versão). Não faça edições independentes nas cópias.
3. Clone `mullz013/eixo-piloto-01`; execute `claude --agent eixo-orchestrator` no diretório do piloto, em uma versão que suporte essa opção.
4. Solicite: “Verifique os seis agentes instalados, leia o DNA DRAFT e handoffs, proponha pendências e **aguarde a aprovação do briefing**.”
5. Após a aprovação do Project DNA, valide o fluxo com delegações reais, registrando comandos, logs de execução, arquivos gerados e PRs.

O GitHub Actions apenas valida JSON, estrutura, dependências e bloqueio de release. Não executa modelos Claude e não exige segredos/API keys.
