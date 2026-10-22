# Registros de handoff

Status válidos: `PENDING`, `BLOCKED`, `IN_PROGRESS`, `READY_FOR_REVIEW`, `COMPLETED_VERIFIED`, `FAILED`.

Cada agente registra as tarefas em `state.json` e cria `<task_id>.md` com artefatos, URLs verificáveis, versão de DNA, critérios de aceite, riscos e evidências. **Nunca marcar `COMPLETED_VERIFIED` sem evidência real.**

A primeira execução real dos agentes está registrada em `ORCH-001.md`, com extratos do runtime em `evidence/ORCH-001/`. O workflow de CI verifica integridade da estrutura e dessas evidências; ele não executa agentes.
