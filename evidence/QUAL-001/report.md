# QUAL-001 · Revisão qualitativa de UX, UI, conteúdo e acessibilidade

**Projeto:** piloto-01 (Ateliê Bruma, marca fictícia) · **DNA:** v0.2.0 · **Papel:** eixo-quality-specialist (executado por subagente com a definição de `mullz013/eixo-ai/.claude/agents/eixo-quality-specialist.md`)
**Commit verificado:** `1159d06` (branch `claude/project-thread-8m8hi1`), sem alterações locais em `site/`
**Data:** 2026-10-22 · **Ambiente:** Playwright (Python, sync) + Chromium 1194 headless, Linux. Página servida por `python3 -m http.server` em `127.0.0.1:8765` (também aberta em `file://` para comparar)

> Nota de registro: o subagente não pôde gravar este arquivo; o texto é o relatório dele, salvo sem alteração de conteúdo pela sessão coordenadora.

## Veredito: **PASS_WITH_NOTES**

Nenhum P0 ou P1. A jornada P0 (banner → categorias/vitrine → adicionar → sacola → "Finalizar compra" com aviso de loja demonstrativa) funciona no celular e no desktop. As preferências do proprietário estão quase todas atendidas. Três P2 pedem correção antes da aprovação humana; o resto é polimento ou gosto.

(O papel define `PASS / CHANGES_REQUIRED / BLOCKED`. Esta tarefa pediu `PASS / PASS_WITH_NOTES / FAIL`. Em termos do papel, PASS_WITH_NOTES equivale a PASS condicionado à correção ou ao aceite explícito dos P2.)

Esta é uma análise de especialista. **Não é teste com usuários** e não traz resultados de usabilidade. Aprovação de Quality também não é um `GO` técnico do QA.

| Severidade | Quantidade |
|---|---|
| P0 | 0 |
| P1 | 0 |
| P2 | 3 |
| P3 | 14 |
| Sugestões de gosto (sem severidade) | 8 |

## 1. O que foi verificado (e como)

| Verificação | Como | Resultado | Evidência |
|---|---|---|---|
| Render visual em 375, 768 e 1440 (página inteira e por seção) | Capturas olhadas uma a uma | Ver achados | `full-*.png`, `fold-*.png`, `sec-<largura>-<seção>.png` |
| Rolagem horizontal da página | `scrollWidth` em 320, 375, 768 e 1440 | Nenhuma | `measures.json`, `interactions.json` |
| Margens e simetria no celular | Bounding boxes em 320, 375, 414, 768, 1024 e 1440 | Simétricas (esquerda = direita em todos os blocos) | `margins.json` |
| Carrossel 4 / 2 + corte | Contagem de cartões inteiros e fração do próximo | 1440: 4 inteiros, sem corte visível; 768: 3 + 46%; 375: 2 + 30% | `measures.json` |
| Menu hambúrguer (375) | Clique, Tab ×25, Esc | Foco preso na gaveta, Esc fecha e devolve o foco a "Abrir menu" | `int-375-menu.png`, `interactions.json` |
| Sacola | Adicionar 2 peças, abrir, finalizar | Contador = 1 e depois 2, aviso "Caneca Névoa foi para a sacola", subtotal R$ 226, barra "Faltam R$ 73", aviso de loja demonstrativa | `int-375-added.png`, `int-375-cart.png`, `int-375-checkout.png` |
| Sacola vazia por teclado (1440) | Tab até a sacola, Enter, Tab ×6, Esc | Foco preso (Fechar ↔ Ver novidades), Esc devolve o foco ao botão Sacola | `int-1440-cart-empty.png` |
| Filtro por categoria | Toque em "Pratos" | Barra "Mostrando: Pratos · Limpar filtro" e 3 cartões (bate com "3 peças") | `int-375-filter.png` |
| Ordem e visibilidade do foco (1440) | Tab ×45, com e sem espera pela rolagem suave | Anel de 3 px `#25231F` em todos. O elemento focado entra na tela depois da rolagem suave | `interactions.json`, `int-1440-focus-*.png` |
| Nomes acessíveis | Árvore de acessibilidade via CDP | Ver P2-3 e P3-9/10 | `ax-names-1440.txt` |
| Movimento | `getAnimations()` | Padrão: 3 animações `drift` em loop. Com "Pausar animação": 0, e o botão vira "Retomar animação" com `aria-pressed=true`. Com `prefers-reduced-motion: reduce`: 0 | `interactions.json` |
| Sem JavaScript (375) | JS desligado | Links de navegação visíveis no lugar do hambúrguer, página legível | `int-375-nojs.png` |
| Espaçamento de texto (WCAG 1.4.12) em 640 px (≈ zoom de 200% sobre 1280) | CSS de teste: line-height 1.5, letter-spacing .12em, word-spacing .16em | Sem rolagem horizontal e sem corte visível no trecho inspecionado | `int-640-textspacing.png` |
| Scanner axe-core 4.10.2 (wcag2a/aa, 21aa, 22aa) em 320, 375 e 1440 | Injetado na página | 0 violações. `color-contrast` ficou "incomplete" em 96 a 107 nós (texto sobre imagem ou gradiente): **o scanner não decide esses casos** | `interactions.json` |
| Contraste do texto do banner sobre a foto | Pixels amostrados com o texto transparente, movimento reduzido | Ver P2-2 | `hero-contrast-sampled.json` |
| Copy em português | Leitura de todo o texto visível, dos `alt` e da ajuda | Ver achados | `site/index.html` |

Os scripts de captura estão em `capture-scripts/`.

Nota sobre as capturas de página inteira: as fotos de "Terra Molhada" e "Sal" aparecem vazias em `full-*.png` por causa do `loading="lazy"` nativo durante a captura. Depois de rolar até elas, as imagens carregam (`full-1440-after-lazyload.png`, `sec-*-colecoes.png`). É limitação da captura, não defeito.

### NOT_RUN (não verificado nesta revisão)
- Leitor de tela real (NVDA, VoiceOver, TalkBack).
- Aparelhos reais, gesto de arrastar com o dedo, Safari e Firefox.
- Zoom real de 200% e 400% do navegador. Só houve a aproximação por largura de viewport (320 e 640 px).
- Contraste de texto sobre imagem fora do banner. É um dos itens que o axe deixou como "incomplete".
- Contraste do banner **durante** a animação da névoa: a amostragem foi feita parada.
- `forced-colors`, `prefers-contrast` e modo escuro do sistema.
- Desempenho (LCP, CLS). É escopo do QA.
- Comparação com o Figma: não há frame de referência para este layout.

## 2. Preferências do proprietário: conferência

| Preferência | Situação | Observação |
|---|---|---|
| Hambúrguer no celular | OK | Abaixo de 1024 px, gaveta à esquerda com os grupos "Por peça" e "Por momento" |
| Margens simétricas no celular | OK | Medido em 320 (16/16), 375 (18,75/18,75), 414 (20,7/20,7) e 768 (32/32) |
| Vitrine: 4 no desktop, 2 + corte no celular | OK | 375: 2 + 30% do 3º, com bullets e sem setas. 1440: 4, com setas e bullets |
| Sem placeholders | OK | Todas as imagens são fotos (DES-001). Nenhum placeholder visível |
| Banner com margens iguais em todos os lados | **Não atende**, ver P2-1 | Topo de 12 px contra 18,75 px nas laterais e embaixo (375); 12 contra 32 (768) |
| Tags acima dos títulos no Badge (pílula) do design system | OK na forma | Pílula de raio 999 em todas. Ver P3-8 (12 px) e a sugestão S1 (caixa-alta) |
| Títulos de seção mais fortes | OK | Fraunces 500 a 40 px (era 400). Ver S2 sobre o itálico em 300 |
| Sem círculo colorido ao lado do título das coleções | OK | "Terra Molhada" e "Sal" só têm a pílula da estação acima |

## 3. Achados: defeitos reais

**P2-1 · O banner não tem a mesma margem nos quatro lados (preferência do proprietário).**
- **Onde:** `.hero`, em todas as larguras. Medido (`margins.json`): topo (header até o banner) / laterais / base (banner até a faixa de vantagens): 320: 12 / 16 / 16; 375: 12 / 18,75 / 18,75; 768: 12 / 32 / 32; 1440: 16 / alinhado ao container / 32.
- **Por que importa:** o proprietário pediu explicitamente margens iguais em todos os lados. O topo mais curto deixa o painel colado no header.
- **Recomendação:** `margin-top` do `.hero` = `var(--panel-gap)`. Teste: topo = lateral = base em 320, 375, 768 e 1024; no desktop, topo = base.

**P2-2 · Texto de apoio do banner com contraste no limite sobre a foto (1440).**
- **Onde:** `.hero__lead`, `#55514A`, cerca de 21 px, peso regular: não conta como texto grande.
- **Medido** (fundo amostrado sem o texto, animação parada): mínimo de 4,47:1, percentil 5 de 4,82:1, mediana de 5,8:1. Em 375 o mínimo é 5,08 e em 768 é 4,93. Os pontos mais fracos ficam no fim das linhas 1 e 2, onde o texto encosta na pedra clara da foto. A névoa se move, então o pior caso real pode ser menor. Isso não foi medido.
- **Por que importa:** WCAG 1.4.3 pede 4,5:1, e o axe não consegue decidir texto sobre imagem.
- **Recomendação:** limitar `.hero__lead` a cerca de 30ch no desktop, ou reforçar a névoa ou o degradê atrás da coluna de texto, ou usar `--text-primary`. Teste: mínimo ≥ 4,5:1 em 1280, 1440 e 1920, com a névoa em duas posições.

**P2-3 · O nome acessível de "Adicionar à sacola" não contém o rótulo visível (WCAG 2.5.3).**
- **Onde:** `button.add` (18 botões). Visível no desktop: "Adicionar à sacola" (com `aria-hidden`). Nome acessível: "Adicionar Caneca Névoa à sacola", que parte a expressão visível.
- **Por que importa:** quem usa comando de voz diz o que vê, e o nome não contém essa sequência. No celular o rótulo "Adicionar" está contido no nome, então lá está correto.
- **Recomendação:** "Adicionar à sacola: Caneca Névoa", com o rótulo visível fora do `aria-hidden` e o nome da peça em `sr-only`. Corrigir também o estado confirmado (hoje o nome vira "Adicionada Adicionar Caneca Névoa à sacola").

- **P3-1** · "Toque numa categoria" aparece no desktop (`#categorias`). Usar "Escolha uma categoria…", que serve aos dois contextos.
- **P3-2** · Formato de parcela inconsistente: "3x de R$ 56", "R$ 62" e "R$ 70" ao lado de "R$ 32,67". Usar sempre duas casas decimais.
- **P3-3** · A sacola vazia mostra "Faltam R$ 299 para o frete grátis". Esconder a barra enquanto a sacola estiver vazia.
- **P3-4** · Ordem de foco no desktop: "Pausar animação" (embaixo à direita) recebe foco antes de "Comprar a coleção" (2.4.3). Mover o botão para depois de `.hero__copy` no DOM.
- **P3-5** · Em 375 e 768, "Pausar animação" cobre o topo do vaso. Usar um botão só de ícone (alvo de 44 px, nome acessível mantido) ou levá-lo para o canto inferior.
- **P3-6** · Banner em 768: a imagem quadrada do celular, esticada para 704 px, corta o vaso da esquerda, perde o disco terracota e fica levemente desfocada. Usar a imagem 3:2 a partir de cerca de 600 px, ou ajustar o `object-position`.
- **P3-7** · A faixa do topo em 768 quebra com "processada" sozinha na segunda linha. Esconder `.announce__long` até 1024 px ou usar `text-wrap: balance`.
- **P3-8** · `.tag` e `.badge` em 12 px, `.bag-btn__count` em 11 px. A direção de arte (§5.4) pede no mínimo 13 px; o UI-004 adotou 12 px ao seguir o Badge do shadcn. Registrar a exceção ou voltar para 13 px. O contador deve ir para no mínimo 12 px.
- **P3-9** · O botão desabilitado "Esgotado" não diz de qual peça é. Usar "Esgotado: Prato raso Terra Molhada" via `sr-only`.
- **P3-10** · Nomes acessíveis "Ateliê Bruma , início" e "Sacola , 0 itens" têm espaço antes da vírgula. Tirar o espaço no `sr-only`.
- **P3-11** · A faixa de vantagens diz "em até 3x sem juros", mas omite "a partir de R$ 90", que está na Ajuda.
- **P3-12** · Rodapé "Pagamento" e Ajuda "Formas de pagamento": uniformizar.
- **P3-13** · Abrindo por `file://`, os 3 `<link rel="preload" crossorigin>` dão erro de CORS no console. As fontes carregam mesmo assim (`document.fonts` = loaded). Não afeta o usuário; anotar no runbook que a revisão deve ser feita por HTTP local.
- **P3-14** · `art-direction.md` §5.5 ("sem sombras", "pílula só no CTA") e §5.8 ("nenhuma animação ambiente de névoa") estão superados pela UI-003, mas não estão marcados como tal. Marcar e linkar `revisao-003.md`, para que ninguém "corrija" o site de volta.

## 4. Sugestões de gosto (não são defeitos)

- **S1** · Tags em caixa-alta com espaçamento: o Badge do shadcn é em caixa normal, peso 500, sem tracking. A forma já segue o design system, a tipografia não. Decidir e registrar.
- **S2** · O título está em 500 e o itálico de ênfase em 300: a palavra destacada parece mais fina que o resto. Testar o itálico em 400.
- **S3** · "Terra Molhada" e "Sal" são faixas de borda a borda, enquanto o resto da página usa painéis arredondados. Usar painéis tingidos dentro do container.
- **S4** · `alt=""` nas fotos de produto: o esmalte é o que vende a peça. Um alt curto descrevendo o esmalte ajudaria quem usa leitor de tela.
- **S5** · "Novo" em só 2 das 8 peças de "Novidades da fornada". Usar em todas, em nenhuma, ou trocar por um selo com significado.
- **S6** · Em 375, "3x de R$ 32,67 sem / juros" quebra no cartão. Usar `nowrap` ou a forma curta.
- **S7** · A linha da mesa nas fotos dos pratos fica mais alta que nas outras peças e quebra o ritmo da fileira. Fica para a próxima rodada de fotos.
- **S8** · Na Ajuda, "enviamos outra" contradiz "nenhuma é igual à outra". Usar "enviamos uma peça equivalente ou devolvemos o valor".

## 5. Leitura qualitativa

- **Marca:** coerente com a direção "Névoa quieta". A argila aparece só em ação e ênfase, a Fraunces e a Figtree estão bem usadas, e a fotografia é consistente por coleção. A identidade da EIXO não aparece. O caráter fictício está visível na faixa do topo, no rodapé e no aviso de "Finalizar compra", sem deixar a página com cara de quebrada.
- **Heurísticas de Nielsen (pontos fortes):** o estado do sistema é visível (contador, aviso, barra de frete, "Mostrando: X"); o usuário tem controle (Limpar filtro, Remover, quantidade, Pausar); há consistência entre as três vitrines; os erros são prevenidos (Esgotado desabilitado).
- **Pontos fracos:** P2-1, P2-2 e a coerência de copy (P3-1, 2, 11 e 12).
- **Honestidade:** não há depoimentos, estrelas, urgência inventada ou contagem de gente.

## 6. Responsáveis e reteste

| Achado | Responsável | Reteste |
|---|---|---|
| P2-1, P3-4 a P3-7, S2, S3 | UI + Developer | Capturas em 320, 375, 768 e 1440 + `margins.json` |
| P2-2 | UI + Developer | Amostragem de contraste do banner em 1280, 1440 e 1920, com a névoa em duas posições |
| P2-3, P3-9, P3-10 | Developer | Árvore de acessibilidade (CDP) e, se possível, NVDA ou VoiceOver |
| P3-1 a P3-3, P3-11, P3-12, S5, S8 | UX (copy) + Developer | Leitura de copy |
| P3-8, S1 | UI (decisão registrada) | Nenhum |
| P3-13, P3-14 | Orchestrator / UI (documentação) | Nenhum |

Quality não alterou código. Nada foi commitado nem enviado.
