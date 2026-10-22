# DEV-001 — Verificação independente (sessão coordenadora)

**Data:** 2026-10-22 · **Quem:** sessão Claude Code que coordena o piloto (não o Developer, não o QA). Isto **não** é o parecer de QA-001 nem de QUAL-001.
**Ambiente:** container Linux, Chromium headless 1194 via Playwright (Python), arquivo local `site/index.html` (file://). Scripts não versionados; resultados brutos em `render/render-check.json` e `render/interaction-check.json`.

## Autoria da delegação
`delegation-transcript.json`: init do runtime lista os 6 agentes eixo-*; o `eixo-orchestrator` chamou `Agent` com `subagent_type: eixo-fullstack-developer` em primeiro plano, e as chamadas do Developer (12 Read, 8 Write, 2 Edit, 1 Grep, 3 Bash somente leitura) carregam `parent_tool_use_id`. Resultado: `success`, 10 turnos do orquestrador, ~358 s, ~US$ 1,23. O stream bruto não foi versionado.

## Resultados (EXECUTED)

| Check | Resultado |
|---|---|
| Rolagem horizontal 320, 375, 768, 1024, 1440 | **Nenhuma** (`scrollWidth` = largura em todas) |
| Fontes | Fraunces e Figtree `loaded` em todas as larguras (fallbacks `local()` ausentes no container, esperado) |
| Recursos externos / erros de console | **0** / **0** |
| Header | 57 px de altura, uma linha em todas as larguras, inclusive 320 px com Figtree real |
| AC-P0-01 CTA na primeira tela | 375 × 667: base do CTA em 460 px ✔ · 320 × 568: 460 px ✔ (folga 108 px) |
| AC-P0-02 CTA → `#colecao` | hash `#colecao`, h2 "Coleção Névoa" visível abaixo do header (topo 224 px a 375; 272 px a 1440), foco em `section#colecao` |
| AC-P0-04 Contato / Material pelo header | hash correto, h2 visível abaixo do header, foco na `section` |
| AC-NAV-01 Skip link | primeiro Tab, visível ao focar (`skiplink-focus-*.png`), aponta para `#conteudo` |
| Ordem de Tab | skip → marca → Coleção → Material → Contato → CTA → e-mail → marca (rodapé) → Voltar ao início (8 paradas, sem armadilha) |
| axe-core 4.10.2 (wcag2a/aa, 21a/aa, 22aa, best-practice) | **0 violações**, 44 regras passando, 0 incompletas, a 375 e 1440 |
| WCAG 1.4.12 espaçamento de texto a 320 px | sem rolagem horizontal |

## Observações para QA-001 / QUAL-001 (não corrigidas aqui)
- **F1 (UI, baixa):** o "(exemplo)" dos preços herda Fraunces de `.piece .price`; o handoff §5.5 pede Figtree 500 14 px. Correção provável: `font-family: var(--stack-text)` em `.ex`.
- **F2 (UX, baixa):** ao chegar por âncora, o h2 fica ~170–215 px abaixo do header (o `scroll-margin` está na `section`, cujo padding superior soma ao offset). Visível, mas com mais espaço que o previsto (§3 do handoff: h2 a ~80 px).
- **F3 (a11y, revisão humana):** foco programático vai para a `section` com `outline:none` (desvio D1). axe não acusa; a decisão é da UI/Quality.
- Não testado: leitor de tela, zoom real 200/400 %, Safari/Firefox, LCP/CLS em rede real, validação HTML do W3C.

## Screenshots
`render/viewport-{320,375,768,1024,1440}.png`, `render/fullpage-{375,1440}.png`, `render/skiplink-focus-*.png`, `render/apos-cta-*.png`.
