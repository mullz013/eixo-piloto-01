# EIXO — Piloto 01

Repositório **privado** para validação da esteira EIXO multiagente. Os seis agentes, comandos e políticas reutilizáveis ficam no repositório central `mullz013/eixo-ai`. Este repositório armazena somente o código, o briefing e as evidências do piloto.

## Situação
- **Project DNA**: `APPROVED` (v0.2.0) — marca **fictícia**, aprovado apenas para teste controlado; UX/UI ainda pendentes.
- **Criação deste repositório**: manual. O provisionamento automático ainda não foi testado no GitHub remoto.
- **Agentes trabalhando**: ainda NÃO executados em runtime Claude Code.
- **Deploy de produção**: BLOQUEADO.

## Passos para executar
1. Revisar o [DNA v0.2.0 já aprovado](docs/project-dna.md) e manter o escopo fictício.
2. Instalar seis agentes do repositório EIXO central segundo `docs/runtime-setup.md`.
3. Iniciar o Claude Code com o Orchestrator e delegar tarefas reais com handoffs.
4. Executar `python scripts/validate_pilot.py` e `python -m unittest discover -s tests -v`.
5. Abrir PRs de UX/UI/implementação, revisar gates e documentar evidências.

**Testes verdes de estrutura não significam que um site foi implementado ou aprovado.**
