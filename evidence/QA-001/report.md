# QA-001 · Testes reais automatizados

**Papel:** eixo-qa-engineer (executado por subagente com a definição de `mullz013/eixo-ai/.claude/agents/eixo-qa-engineer.md`).
**Commit verificado:** `1159d06` · **Data:** 2026-10-22 · **Veredito:** **FAIL (NO_GO)**.
O relatório completo, com o bloco JSON para o Orchestrator, está em [`report.json`](report.json). As capturas ficam fora do repositório, em `/mnt/project-files/eixo-piloto/qa-001/`, para não pesar o git.

## Execuções em 1159d06
- unittest: 8/8 OK. `validate_pilot.py`: exit 0.
- `qa_test.py` (82 checagens): 79 PASS / 3 FAIL por HTTP; 77 / 5 em `file://` (as 2 extras são fontes bloqueadas por CORS em origem null, não é defeito).
- axe-core 4.10.2 em 9 estados: 0 violações.

## Achados
- **P1 · BUG-01:** CTA "Comprar a coleção" fora da primeira tela no celular (375×667: 682–734 px). Reprova AC-P0-01/M1.
- P3 · BUG-02: sem JS, o header de ~160 px cobre o título de destino da âncora.
- P3 · BUG-03: espaço antes da vírgula em "Ateliê Bruma , início" e "Sacola , 1 item".

## NOT_RUN
Lighthouse 4G, Core Web Vitals de campo, Firefox/WebKit e aparelhos reais, leitor de tela, zoom 200/400%, validador W3C, baseline visual, toque real, sacola sem localStorage.

## Correções do Developer depois de 1159d06 (aguardam reteste independente)
- BUG-01: o proprietário escolheu "foto mais baixa no celular" (2026-10-22). `.hero__stage` passou a `clamp(150px, 40vw, 320px)`; o CTA termina em 654 px em 375×667. Em 320×568 e 360×640 continua abaixo da dobra, fora do escopo da decisão.
- BUG-02: `--anchor-offset` de 184 px sem JS abaixo de 1024 px.
- BUG-03: nomes sem espaço ("Ateliê Bruma, início", "Sacola, N itens").
- Do Quality: o botão de compra agora se chama "Adicionar à sacola: <peça>" (WCAG 2.5.3). **O T19 do `qa_test.py` ainda espera o nome antigo e precisa ser atualizado pelo QA no reteste.**
- Pré-execução pelo Developer (`--tag reteste-http`, sem axe): 70 PASS / 3 FAIL (T19 por causa do nome esperado, T21-320 fora do escopo, T22 antes desta correção). Isso não substitui o reteste do QA.
