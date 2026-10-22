# ORCH-001 — Bootstrap do runtime multiagente

**Status:** COMPLETED_VERIFIED — runtime Claude Code executado e primeira delegação real registrada em 2026-10-21.

**Entrada:** Project DNA v0.2.0 aprovado (somente briefing fictício).
**Saída:** inventário dos seis agentes no runtime e uma delegação real do `eixo-orchestrator` ao `eixo-ux-architect` (probe somente leitura). UX-001 completo segue como tarefa própria.

## Ambiente
- Claude Code 2.1.307, container na nuvem do Claude Code; diretório do piloto, branch base `eixo/bootstrap-pilot-v1` (d79c3a6).
- Agentes copiados de `mullz013/eixo-ai` @ `eixo/setup-multiagent-v1.1` (2b4a012) para `.claude/agents/` (cópia local, não versionada, como manda `docs/first-run-command.md`).
- Modelo efetivo: `claude-sonnet-5-5` (agentes usam `model: inherit`).

## Execução 1 — inventário
```bash
claude --agent eixo-orchestrator -p "Liste apenas os nomes de subagentes disponíveis para a ferramenta Agent nesta sessão..." \
  --output-format stream-json --verbose --max-turns 2
```
O evento `init` do runtime listou: `eixo-fullstack-developer`, `eixo-orchestrator`, `eixo-qa-engineer`, `eixo-quality-specialist`, `eixo-ui-art-director`, `eixo-ux-architect` (além dos agentes nativos). Evidência: [`evidence/ORCH-001/inventory.json`](../evidence/ORCH-001/inventory.json).

## Execução 2 — primeira delegação real
```bash
claude --agent eixo-orchestrator --allowedTools "Agent Read Glob Grep" --disallowedTools "Write Edit Bash" \
  --max-turns 8 --output-format stream-json --verbose -p "ORCH-001 (prova de runtime) ... task_id ORCH-001-PROBE ..."
```
- O orchestrator chamou `Agent` com `subagent_type: eixo-ux-architect` (`toolu_01BvBtKBTkVgA1U62PXvExXv`).
- O subagente executou `Read` em `docs/project-dna.md` e `docs/project-dna.json`; os dois eventos têm `parent_tool_use_id = toolu_01BvBtKBTkVgA1U62PXvExXv`, o que prova que a execução foi do subagente, não roleplay do orchestrator.
- O subagente devolveu `artifacts/status/evidence/risks/blockers/next_action`; nenhuma escrita (ferramentas de escrita bloqueadas).
- Citações conferidas manualmente: jornada P0 e CTA em `docs/project-dna.md` linhas 11–12; `primary_cta` e `assets_approved: false` em `docs/project-dna.json`.
- Custo do run: ~US$ 0,23, 2 turnos do processo principal.

Evidência: [`evidence/ORCH-001/delegation-transcript.json`](../evidence/ORCH-001/delegation-transcript.json) (extrato do stream-json: init, tool_use/tool_result com `parent_tool_use_id` e resultado final).

## Perguntas bloqueantes levantadas pelo UX Architect para UX-001
1. Seção de contato demonstrativo: só informações estáticas fictícias ou formulário sem envio real (com estados simulados)?
2. Coleção fictícia: quantas peças, quais campos, e imagens como placeholders até definição de licença?
3. Critérios mensuráveis: há métricas para o piloto ou apenas aceite funcional Dado/Quando/Então?

## Critérios de aceite
1. ✅ Claude Code rodou no diretório do piloto, com agentes do `eixo-ai` instalados.
2. ✅ Lista real de agentes consultada no runtime (evento `init`), sem roleplay.
3. ✅ Delegação real ao UX Architect com autoria verificada por `parent_tool_use_id`. UX-001 completo continua `PENDING`, em tarefa própria.
4. ⏳ Handoff UX-001 e gate humano: responsabilidade de UX-001, antes de avançar para UI.

## Limites
- Não houve escrita de arquivos pelos agentes, deploy, serviços pagos nem acesso a outros repositórios.
- `scripts/eixo.py gate` do `eixo-ai` avalia o formato `projects/<id>/handoffs/<stage>.json` e ainda não lê o formato deste piloto; o gate aplicável aqui é `python scripts/validate_pilot.py`.
