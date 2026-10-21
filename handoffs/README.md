# Registros de handoff

Status válidos: `PENDING`, `BLOCKED`, `IN_PROGRESS`, `READY_FOR_REVIEW`, `COMPLETED_VERIFIED`, `FAILED`.

Cada agente registra as tarefas em `state.json` e cria `<task_id>.md` com artefatos, URLs verificáveis, versão de DNA, critérios de aceite, riscos e evidências. **Nunca marcar `COMPLETED_VERIFIED` sem evidência real.**

Este repositório foi criado manualmente e ainda não executou agentes de IA. O workflow de CI verifica integridade da estrutura, não colaboração real entre agentes.
