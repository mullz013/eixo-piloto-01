# Roteiro do ensaio multiagente

1. **Orchestrator:** verificar agentes instalados, confirmar que Project DNA v0.2.0 já foi aprovado como briefing fictício; verificar agentes instalados, credenciais e registrar primeira delegação REAL (evidências).
2. **UX Architect:** produzir jornadas, arquitetura de informação, conteúdo e critérios de aceite (revisão/aceite).
3. **UI Designer & Art Director:** direção de arte própria, tokens, layouts e estados acessíveis (revisão/aceite).
4. **Developer:** implementar interface e interações sem descaracterizar arte; documentar execução e testes.
5. **QA Engineer e Quality Specialist:** análises independentes em paralelo, depois da implementação; abrir defeitos e exigir reexecução após correções.
6. **Orchestrator:** verificar evidências rastreáveis e preparar relatório para revisão humana. **Não publicar** sem autorização específica.

## Como demonstrar colaboração real
- Cada especialista deve ter sido invocado efetivamente pelo runtime Claude Code, não apenas citado em texto.
- Cada handoff deve referenciar artefatos (commit, PR, frames ou relatórios) e evidências.
- Registrar ao menos um defeito, correção e reteste na fase de QA.
- A criação remota automática de outro repositório de teste permanece separada e pendente.

## Estado inicial verificável
`DNA_APPROVED_RUNTIME_UNVERIFIED`, DNA `APPROVED` (briefing fictício), ORCH-001 `BLOCKED` até runtime comprovado, todos os outros pacotes de trabalho `PENDING`, release desabilitado.
