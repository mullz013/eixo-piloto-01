# Correções após o parecer do eixo-qa-engineer (QA-002)

**Data:** 2026-10-22 · **Parecer:** `parecer-qa.md` (NO-GO, 22 achados, análise só por leitura)
**Reteste:** Playwright + Chromium, servidor http local, `evidence/DEV-002/render/interaction-check.json` (chaves citadas abaixo). O reteste foi feito pela sessão do projeto, não pelo QA; um reteste independente ainda é recomendado.

| ID | Disposição | Como foi resolvido | Evidência |
|---|---|---|---|
| QA-01 | Corrigido | Rótulo "Sacola" escondido com técnica sr-only (não `display:none`), contador visual `aria-hidden` | `m_bag_accessible_name` = "Sacola , 0 itens" em 375 px |
| QA-02 | Corrigido | Regra global em `prefers-reduced-motion` zera animações e transições; `matchMedia` reage a mudanças | `reduced_motion_after_add_animations` = 0 |
| QA-03 | Corrigido | Botão "Pausar animação" (`aria-pressed`) no banner; some com movimento reduzido | `pause_state` = paused / true |
| QA-04 | Corrigido | Rótulos originais guardados em `data-*` e um timer por botão | `m_add_label_after_double_click` = "Adicionar" |
| QA-05 | Corrigido | Nome acessível com a peça; textos curto/longo em spans `aria-hidden` | `m_add_accessible_name` = "Adicionar Caneca Névoa à sacola" |
| QA-06 | Corrigido | Foco vai para o título "Compre por categoria" | `m_focus_after_clear_filter` = t-categorias |
| QA-07 | Corrigido | Setas usam `aria-disabled` e continuam focáveis | `d_next_focusable_at_end` = true |
| QA-08 | Corrigido | Sacola só aceita itens do catálogo; nome, preço e imagem vêm do botão; quantidade inteira de 1 a 20 | `m_bad_storage_count` = 0; `m_tampered_storage` = 3 itens, R$ 216 (preço adulterado ignorado) |
| QA-09 | Corrigido | Classe `no-js`: menu visível em todas as larguras, controles de compra ocultos | `nojs_nav_visible`, `nojs_add_hidden`; `render/sem-js-375.png` |
| QA-10 | Corrigido | Capturas refeitas aguardando todas as imagens | `render/pagina-1440-full.png`, `render/pagina-375-full.png` |
| QA-11 | Corrigido | Bullet inativo `#8C857A`: 3,24:1 sobre `#F4F1EC` (calculado por script, fórmula WCAG) | este arquivo |
| QA-12 | Corrigido | `inert` em faixa, header, main e rodapé com gaveta aberta | `m_main_inert_when_drawer_open` = true, `..._after_close` = false |
| QA-13 | Corrigido | `scroll-padding-top` maior com filtro ativo (`html.has-filter`) | leitura de CSS |
| QA-14 | Corrigido | Link para vitrine escondida limpa o filtro antes de navegar | `m_menu_link_clears_filter` = true |
| QA-15 | Corrigido | Setas e bullets com o nome da coleção; bullets em `role="group"` rotulado | `index.html` |
| QA-16 | Corrigido | Peças das coleções passadas em h4 | `index.html` |
| QA-17 | Corrigido em parte | Header a 97% de opacidade. A faixa sob o header ao saltar para âncora é o respiro da seção e foi mantida | capturas |
| QA-18 | Mantido | Só afeta janelas de desktop estreitas com barra de rolagem clássica; no celular a barra é sobreposta | - |
| QA-19 | Corrigido | Abaixo de 360 px o botão reduz gap, padding e ícone | leitura de CSS |
| QA-20 | Corrigido | Celular mostra "Loja demonstrativa" na faixa; "sem juros" mantido; textos de pedido/frete ajustados; menu rotulado "Menu principal" | `index.html` |
| QA-21 | Corrigido | Comentário de tokens atualizado; gerador grava só as 20 ilustrações usadas | `site/tokens.css`, `scripts/gerar_pecas.py` |
| QA-22 | Corrigido em parte | `scrollbar-gutter: stable`; `addListener` como fallback. Desempenho em celular fraco não foi medido | - |

Aprovação formal de UX-002 e UI-002, apontada pelo QA como ausente, depende do proprietário: os documentos de revisão vão junto na PR #8 para essa decisão.
