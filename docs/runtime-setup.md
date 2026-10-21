# Instalar e executar os agentes

Os seis agentes estão no repositório privado `mullz013/eixo-ai` (branch `eixo/setup-multiagent-v1.1` até merge na `main`).

1. Instale Claude Code, Git e o GitHub CLI no seu computador; autentique `gh auth login`.
2. Clone o `eixo-ai` e instale as seis definições `.claude/agents/*.md` na configuração do Claude Code (por exemplo, no diretório de agentes do usuário, se disponível nessa versão). Não faça edições independentes nas cópias.
3. Clone `mullz013/eixo-piloto-01`; execute `claude --agent eixo-orchestrator` no diretório do piloto, em uma versão que suporte essa opção.
4. Solicite: “Verifique os seis agentes instalados, leia o DNA **APPROVED v0.2.0** e os handoffs, verifique os agentes reais e **delegue somente UX-001 após registrar ORCH-001 com evidências**. Não invente execução; aguarde aprovação humana de UX/UI antes do desenvolvimento.”
5. Como o Project DNA está aprovado, valide o runtime e faça a primeira delegação real ao UX Architect; registre comandos, logs de execução, arquivos gerados e PRs. Sem UI aprovada, não implemente a versão final.

O GitHub Actions apenas valida JSON, estrutura, dependências e bloqueio de release. Não executa modelos Claude e não exige segredos/API keys.
