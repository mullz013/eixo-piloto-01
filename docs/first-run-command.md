# Primeiro ensaio real no Claude Code

## Pré-requisitos
- GitHub e `gh` autenticados na conta com acesso aos repositórios privados.
- Claude Code instalado e autenticado.
- Git instalado.

## Preparar (terminal local)
```bash
gh repo clone mullz013/eixo-ai
cd eixo-ai
git switch eixo/setup-multiagent-v1.1
cd ..
gh repo clone mullz013/eixo-piloto-01
cd eixo-piloto-01
git fetch origin eixo/bootstrap-pilot-v1
git switch eixo/bootstrap-pilot-v1
mkdir -p .claude/agents
cp ../eixo-ai/.claude/agents/*.md .claude/agents/
claude --agent eixo-orchestrator
```

A cópia de agentes é **local e transitória**; não versioná-la no repositório de cliente. Após aprovação da PR central e merge em `main`, usar agentes dessa branch estável. O comando `claude --agent` depende da versão instalada do Claude Code.

## Cole este pedido no Claude Code
> Sou o proprietário da EIXO. O Project DNA v0.2.0 do piloto Ateliê Bruma está aprovado somente para teste fictício. Leia CLAUDE.md, docs/project-dna.md e handoffs/state.json. Verifique realmente a disponibilidade do eixo-orchestrator e dos outros cinco agentes. Registre o resultado em handoffs/ORCH-001.md com evidências. Se conseguir delegar, inicie exclusivamente UX-001 com o especialista UX Architect, gerando arquitetura da informação, jornada P0, conteúdo demonstrativo e critérios de aceite em docs/ux/. Crie handoff e PR para revisão. Não simule subagentes, não avance para UI/Developer sem gates, não use serviços pagos nem publique.

## Como reconhecer que funcionou
- Invocação real de ferramentas/subagentes no runtime (não uma resposta simulada).
- Arquivos `docs/ux/` + handoffs atualizados com evidência de commit/PR.
- Estado UX-001 só muda após ORCH-001 `COMPLETED_VERIFIED`.
- `python scripts/validate_pilot.py` verde; release continua bloqueado.

Se os agentes não estiverem visíveis, marcar ORCH-001 BLOCKED e interromper; o workflow GitHub Actions isolado não executa LLMs.
