# Handoff UI → Developer: Ateliê Bruma (UI-001)

**Projeto:** piloto-01 · **Task:** UI-001 · **Agente:** eixo-ui-art-director · **Rodada:** 3 · **Data:** 2026-10-22
**DNA:** v0.2.0 (aprovado somente como briefing fictício) · **Depende de:** UX-001 (aprovado pelo proprietário em 2026-10-22; `docs/ux/handoff-ui.md`)
**Status:** **APROVADO** pelo proprietário em 2026-10-22T10:23:04Z ("Sim para as 3 perguntas"; ver `handoffs/approval-log.md`). Marca, logotipo, copy e dados continuam **FICTÍCIOS**. DEV-001 liberado. Deploy continua proibido.

> Legenda: **FATO** (fonte externa citada na pesquisa) · **HIPÓTESE** (a validar) · **FICTÍCIO** (inventado para o piloto) · **DECISÃO** (escolha desta UI, sujeita a aprovação). "Pesquisa §x" = `docs/ux/research/pesquisa-mercado.md`.

## 0. O que foi e o que não foi feito

| Item | Situação |
|---|---|
| Figma | **NÃO REALIZADO.** MCP não conectado. Não existe arquivo, frame nem ID de frame. A entrega é este conjunto de arquivos em `docs/ui/`. |
| Render / inspeção visual | **Por este agente (eixo-ui-art-director): NÃO REALIZADO.** Este agente não abriu nenhum SVG ou HTML em navegador nem rasterizou nada. **Pela revisão independente (sessão que coordena o piloto): a prancha `preview.html` foi renderizada** com Playwright + Chromium headless; resultados em `evidence/UI-001/render-check.json` (e `logo-32px-check.json`): 5 SVGs carregam em 81 × 32 e 32 × 32; header da maquete a 320 px em uma linha (termina em 308 px de 320, **com fonte de fallback**, pois Figtree não está embutida); **rolagem horizontal da prancha em 320, 375, 768 e 1024 px** (scrollWidth ~1058 a 1074), sem rolagem só em 1440. Esse registro mede; **não avalia visualmente** a prancha nem o símbolo. |
| Rolagem horizontal da prancha (rodada 3) | **Corrigida por análise de CSS, não por render.** Causa apontada pela revisão: o item de grid que envolve `.mockscroll` da maquete de 1024 px tinha `min-width:auto`. Correção em `preview.html`: `.grid{grid-template-columns:minmax(0,1fr)}` e `.grid>*{min-width:0}` (mesmo para `.dl`). Este agente **não renderizou nem mediu**; **precisa de nova medição pela revisão** em 320, 375, 768, 1024 e 1440 px. |
| Scripts | **Por este agente: NÃO EXECUTADOS.** As razões de contraste (§7) foram calculadas à mão por este agente (fórmula WCAG 2.x) e **conferidas por script pela revisão independente** (`evidence/UI-001/contrast-check.json`): os 20 pares da tabela conferem, diferença máxima 0,04. C16b (stone-500 sobre mist-300) = 2,56 **falhava**; a borda do placeholder passou a ink-700, que mede 4,43 (`C16b-fix`) e passa. Contraste de cor não equivale a conformidade WCAG. |
| Licenças das fontes | **NÃO verificadas online.** Citadas de conhecimento prévio; o Developer baixa e arquiva os `OFL.txt` (§8). |
| Teste com pessoas | Nenhum. Nada aqui é resultado de usabilidade nem de reconhecimento de marca. |
| Medidas de largura (header, quebras de linha, altura da primeira tela) | **Estimativas** de projeto, rotuladas "estimado". Precisam de medição no navegador. |

## 1. Arquivos desta entrega

| Arquivo | Conteúdo |
|---|---|
| `docs/ui/art-direction.md` | Leitura de marca, curadoria honesta, duas direções, escolha ("Névoa quieta"), sistema visual, crítica, rubrica |
| `docs/ui/tokens.json` · `docs/ui/tokens.css` | Tokens (mantidos à mão, em sincronia; nenhum gerador rodou) |
| `docs/ui/preview.html` | Prancha estática de componentes (não é o site; renderizada só pela revisão, que achou rolagem horizontal, corrigida na rodada 3 sem nova medição) |
| `docs/ui/logo/` | 5 SVGs + `README.md` (conceito, construção, 7 requisitos, **revisão do símbolo em §7**) |
| `docs/ui/ui-handoff.md` | Este arquivo: componentes, estados, layouts, contrastes, assets, pendências |

## 2. Tokens: nomes e uso

Nomes canônicos (idênticos em `tokens.json` e `tokens.css`; em CSS os `/` viram `-`):

| Alias semântico | CSS | Primitive | Hex |
|---|---|---|---|
| `background/canvas` | `--background-canvas` | fog-50 | `#F4F1EC` |
| `background/surface` | `--background-surface` | fog-100 | `#EAE6DF` |
| `background/chip` | `--background-chip` | fog-200 | `#D9D4CB` |
| `background/inverse` | `--background-inverse` | ink-900 | `#25231F` |
| `text/primary` | `--text-primary` | ink-900 | `#25231F` |
| `text/secondary` | `--text-secondary` | ink-700 | `#55514A` |
| `text/link` | `--text-link` | clay-700 | `#8A3F22` |
| `text/inverse` | `--text-inverse` | fog-50 | `#F4F1EC` |
| `text/inverse-secondary` | `--text-inverse-secondary` | stone-300 | `#BDB7AC` |
| `action/primary` · `-hover` · `-active` | `--action-primary…` | clay-700 · clay-800 · clay-900 | `#8A3F22` · `#6F3019` · `#5A2813` |
| `action/on-primary` | `--action-on-primary` | fog-50 | `#F4F1EC` |
| `border/default` (decorativo) | `--border-default` | fog-200 | `#D9D4CB` |
| `border/strong` | `--border-strong` | ink-700 | `#55514A` |
| `focus/ring` · `focus/ring-inverse` | `--focus-ring…` | ink-900 · fog-50 | `#25231F` · `#F4F1EC` |
| (decorativo) `mist-300` | `--mist-300` | | `#B9C4C8` |

O primitive `stone-500` (`#7B756B`) foi **retirado** na rodada 3: era usado só na borda do placeholder e não tem outro uso. `stone-300` permanece (texto secundário em fundo escuro).

Regras: argila **só** em ação (CTA, links, faixas do logotipo principal); `mist-300` nunca em texto nem em componente; sem sombra; sem dark mode (ver §9). Tipografia, escala, espaçamento e raio: `art-direction.md` §5.3 a §5.5.

## 3. Estrutura da página e ids (exatos)

`<body id="topo">` → skip link → `<header>` (`<a>` da marca + `<nav aria-label="Principal">`) → `<main id="conteudo" tabindex="-1">` com `#proposta`, `#manifesto`, `#colecao`, `#material`, `#contato` → `<footer>`. `lang="pt-BR"`. Cada `<section>` com `aria-labelledby` do seu título; cada título que é alvo de âncora com `tabindex="-1"` (foco segue a rolagem, `ux-spec.md` §6.2). `html { scroll-padding-top: var(--anchor-offset) }` e `:where([id]) { scroll-margin-top: var(--anchor-offset) }` (`--anchor-offset` = 5rem = header 56 px + 24 px). Rolagem suave só em `prefers-reduced-motion: no-preference`.

## 4. Princípios que o Developer não pode quebrar

- **CTA único** "Conhecer a coleção" → `#colecao`. Nenhum outro elemento com aparência de botão. Links do header são texto.
- Header com Coleção, Material, Contato **sempre visíveis**; sem hambúrguer. Se a medição real estourar, a rede de segurança é `flex-wrap` (segunda linha), nunca rolagem horizontal.
- Etiquetas "exemplo" e a legenda "Imagem ilustrativa (placeholder)" são texto visível, em caixa sólida, **sem** `display:none`, `visibility`, `clip` nem tamanho zero em nenhum breakpoint.
- Sem depoimentos, estrelas, selos, "mais vendido", carrossel, formulário, segundo CTA, botão de compra, ícones de terceiros, imagens de banco.
- Texto nunca direto sobre o gradiente de névoa: só em caixa sólida.
- Nenhum recurso externo (fontes, scripts, imagens, mapas). Sem JavaScript necessário.

## 5. Componentes e estados

Todos os estados abaixo aparecem em `preview.html` salvo onde indicado. Valores de contraste: §7 (IDs C1, C2…). Movimento: só troca de cor de fundo/texto em 200 ms (`--motion-base`), zerada com `prefers-reduced-motion: reduce`. Foco aparece sem transição.

### 5.1 Header com logotipo

**Anatomia:** barra fixa (`position: sticky/fixed; top: 0`), altura mínima 56 px, fundo `background/canvas` **opaco**, filete inferior 1 px `border/default` (decorativo). Esquerda: link da marca. Direita: `nav`. `z-index` acima do conteúdo e abaixo do skip link.

**Padding lateral:** 12 px abaixo de 360 px; `var(--gutter)` (5vw, entre 16 e 32 px) de 360 px em diante. Gap entre marca e nav: 8 px (320), 12 px (375), livre (≥768, `justify-content: space-between`).

**Link da marca:** `<a class="brand" href="#topo">` com o `logo-principal.svg` (81 × 32 px, tamanho fixo em px, nunca em %/vw) e o texto `<span class="sr-only">, início</span>`. Área clicável `min-height: 44px; min-width: 44px; padding: 6px 4px` (≈ 89 × 44). Raio 10.

| Estado | Marca | Links da nav (Coleção, Material, Contato) |
|---|---|---|
| Padrão | sem fundo | `text/primary`, sem sublinhado, Figtree 600/13 px (<360), 500/14 px (360 a 767), 500/16 px (≥768); `padding-inline` 4 px (<360), 8 px (360 a 767), 14 px (≥768); `min-height: 44px` |
| Hover | fundo `background/hover` (fog-100) | sublinhado 2 px `clay-700`, offset 6 px (não só cor) |
| Foco | contorno 3 px `focus/ring`, offset 2 px, sem transição | idem |
| Ativo | fundo `background/pressed` (fog-200) | sublinhado 3 px + fundo `background/pressed`, raio 4. *Não está na prancha; é especificação.* |
| Imagem falhou | o `alt` "Ateliê Bruma" aparece como texto (`font: 600 13px/32px Figtree; color: text/primary; overflow:hidden`, caixa de 81 × 32) | n/a |
| Monocromático | `logo-mono-fundo-claro.svg` (ink-900) em fundo claro; `logo-mono-fundo-escuro.svg` (fog-50) em fundo escuro, p.ex. rodapé | n/a |

**Nome acessível:** o `<img>` leva `alt="Ateliê Bruma"` e o link fica "Ateliê Bruma, início" (WCAG 2.5.3: contém o texto visível; sem "logotipo"/"imagem"). Alternativa: SVG inline `aria-hidden="true"` com `aria-label="Ateliê Bruma, início"` no `<a>` (então não existe o estado "imagem falhou").

**Símbolo (revisado na rodada 2):** vaso garrafa com lábio, gargalo curto, ombro marcado e base plana. Motivo e limites: `logo/README.md` §7.

**Orçamento de largura da nav (estimado, não medido):**

| Viewport | Padding lateral | Marca (89) + gap | Sobra para a nav | Nav estimada | Folga estimada |
|---|---|---|---|---|---|
| 320 | 24 | 89 + 8 | 199 | ~182 (13 px/600; 4 px de padding) | **~17 px** |
| 375 | 37,5 | 89 + 12 | 236,5 | ~218 (14 px/500; 8 px de padding) | ~18 px |

Estimativa com ~0,54 em por caractere. Se a medição real mostrar folga negativa a 320 px, `flex-wrap: wrap` leva a nav a uma segunda linha. Nesse caso a altura do header passa a 100 px e `--anchor-offset` e `--header-height` precisam ser recalculados (**A CONFIRMAR**).

### 5.2 Skip link

Texto "Pular para o conteúdo" → `#conteudo`. Primeiro elemento focável. Fora da tela até receber foco (`transform`/`clip`, não `display:none`). **Visível ao receber foco:** fundo `background/inverse`, texto `text/inverse` (C10), Figtree 600, `padding: 12px 16px`, raio 10, posição `top: 8px; left: 8px`, contorno 3 px `focus/ring` offset 3 px, `z-index` máximo. Não pode ficar atrás do header. Estados: oculto, foco. Hover/ativo: sem mudança além do cursor. O foco no skip link é suficiente; o `main` recebe foco programático ao ativar.

### 5.3 CTA "Conhecer a coleção"

Único botão de ação. `<a href="#colecao">` (é navegação; não usar `<button>`). Pílula (raio 999), `min-height: 52px`, `min-width: 44px`, `padding: 0 28px`, Figtree 600 17 px / 1,2. Abaixo de 480 px: `width: 100%; max-width: 22rem` (HIPÓTESE: alvo largo no celular ajuda o toque; a validar).

| Estado | Fundo | Texto | Observação |
|---|---|---|---|
| Padrão | `action/primary` (clay-700) | `action/on-primary` (fog-50), C6 | |
| Hover | `action/primary-hover` (clay-800) | fog-50, C7 | transição 200 ms |
| Ativo | `action/primary-active` (clay-900) | fog-50, C8 | |
| Foco | igual ao padrão | | contorno 3 px `focus/ring` offset 3 px; o anel é comparado ao fundo da página, não ao botão (C13) |
| Desabilitado | **não existe** | | não há condição que desabilite |

Limite do componente contra o fundo: clay-700 sobre fog-50, C4 (≥ 3:1).

### 5.4 Links de texto (e-mail, "Voltar ao início")

`text/link` (clay-700), sublinhado 2 px, offset 3 px, Figtree 500; `min-height: 44px` (alvo), `display: inline-flex; align-items: center`.

| Estado | Especificação |
|---|---|
| Padrão e visitado | clay-700 (sem diferença de "visitado"), sublinhado 2 px; C4 em canvas, C5 em surface |
| Hover | clay-800, sublinhado 3 px; C7 em canvas, C14 em surface |
| Foco | contorno 3 px `focus/ring` offset 2 px, raio 4 |
| Ativo | clay-900; C8 em canvas, C15 em surface |
| No rodapé (fundo escuro) | `text/inverse`, sublinhado 2 px; foco com `focus/ring-inverse` (C10, C13b) |

O e-mail é `mailto:` e o **texto do link é o próprio endereço** (`contato@ateliebruma.example`), selecionável. Domínio `.example` reservado: nada é entregue (FICTÍCIO).

### 5.5 Cartão de peça

`<li>` de uma `<ul>` com 6 itens (`ux-spec.md` §5). Sem caixa, sem sombra, sem fundo: filete superior 1 px `ink-900`, `padding-top: 16px`.

Ordem interna (UX): placeholder → h3 → medida → preço → frase de uso.

| Elemento | Especificação |
|---|---|
| Placeholder | §5.6, 4:5, raio 20 |
| h3 (nome) | Fraunces 400, 22 px, 1,2; margem 16 px acima e 4 px abaixo; `text/primary` |
| Medida | Figtree 400, 15 px, `text/secondary` (C2 em canvas) |
| Preço | Fraunces 400, 20 px, `text/primary`, seguido de "(exemplo)" em Figtree 500 14 px, `text/secondary`; o texto completo é "R$ 98 (exemplo)" e não pode perder a etiqueta |
| Frase de uso | Figtree 400, 17 px, `text/secondary` |
| Largura | preenche a coluna; `max-width: 20rem` só se o cartão ficar isolado |

Estados: padrão apenas. O cartão **não é interativo**, então não tem hover, foco, ativo nem cursor de ação (sem botão comprar, ver mais, favoritar). Imagem falhou: §5.6; nome, medida e preço não se movem.

### 5.6 Placeholder de imagem e imagem que falhou

Vale para os 7 placeholders da página (1 hero + 6 peças).

**Padrão:** `div role="img" aria-label="<alt de content-structure.md>"` (ou `<img alt>` quando houver arquivo real, com `width`/`height`). `aspect-ratio: 4 / 5` (fixo, evita CLS), `width: 100%`. Borda 2 px **tracejada** `border/strong` (ink-700; C11, C12, C16 e C16b). Preenchimento: dois gradientes radiais de `mist-300` translúcido sobre degradê vertical fog-100 → fog-200 (decorativo). Raio 20 (peças); hero em arco `999px 999px 10px 10px`.

**Legenda obrigatória:** `<figcaption>` "Imagem ilustrativa (placeholder)" **dentro** da área, canto inferior esquerdo (12 px das bordas), caixa sólida `background/canvas`, texto `text/secondary` 14 px (C2), raio 4, `padding: 6px 10px`. Não ocultável.

**Imagem falhou** (e também modo padrão sem arquivo): contêiner idêntico; o `alt` visível como texto `text/secondary` 14 px **em caixa sólida `background/canvas`** no canto superior esquerdo (12 px), raio 4, `padding: 6px 10px`; legenda permanece embaixo. A proporção 4:5 não muda. (Correção da rodada 2: a prancha anterior pousava o alt direto sobre o gradiente.)

**Contraste da borda (C11, C12, C16, C16b) — resolvido por padrão na rodada 3:** a rodada 2 usava `stone-500`, que o script da revisão confirmou em 3,09:1 contra fog-200 e **2,56:1 contra `mist-300` puro (falha)**. A borda agora é `ink-700`: 7,00 sobre fog-50 (C11), 6,34 sobre fog-100 (C12), 5,35 sobre fog-200 (C16) e **4,43 sobre mist-300 (C16b)**, todos acima de 3:1 (valores do `contrast-check.json`; C11, C12 e C16 coincidem com C2, C3b e C3, que o script mediu). Isso é um **padrão razoável, reversível pelo proprietário** (ver §11, pergunta 8, resolvida por padrão). Custo de design: a borda fica mais escura e presente; **ninguém avaliou visualmente** se o placeholder continua discreto.

**Hero:** mesma coisa, forma de arco, `max-width: 28rem`.

### 5.7 Etiqueta "exemplo"

Retangular (raio 4, para não parecer selo ou medalha), fundo `background/chip` (fog-200), texto `text/primary` Figtree 600 13 px, tracking .02em, borda 2 px **tracejada** `text/secondary` (ink-700; C3, C9). `padding: 3px 8px` (compensa a borda de 2 px). Pode quebrar em várias linhas, nunca truncar nem cortar. O tracejado é a regra visual do projeto: **tudo ilustrativo/fictício tem traço tracejado**. Estados: nenhum (não interativa).

Textos (de `content-structure.md`): "Marca fictícia · página demonstrativa" (hero) · "Preços de referência de exemplo. Não há venda neste site." (coleção) · "Informações de exemplo" (material) · "Dados de exemplo. Este endereço e esta feira não existem." (contato) · "(exemplo)" inline em subtítulo, apoio, preços (Figtree 500 14 px, `text/secondary`) · aviso do rodapé.

### 5.8 Contato

Etiqueta (§5.7) e uma lista de descrição `<dl>`; cada linha `<div>` com `<dt>` (Figtree 600 14 px, `text/secondary`, tracking .02em) e `<dd>` (corpo). Filete superior 1 px `border/default` por linha (decorativo; a separação real é dada pelo `dt`). ≥768 px: grid `11rem 1fr`, gap 16; abaixo: `dt` sobre `dd`, gap 2 px. Largura máx. 40rem. Linhas: E-mail (link §5.4) · Endereço "Rua da Bruma Clara, 214, Curitiba (PR)" (texto, **não é link**, sem CEP, sem mapa) · Cidade · Onde encontrar as peças · Encomendas. Sem formulário, telefone, redes, WhatsApp. Estados: só os do link de e-mail.

### 5.9 Rodapé

Fundo `background/inverse` (ink-900), `padding: 32px 0`. Conteúdo: marca em `logo-mono-fundo-escuro.svg` (link `#topo`, mesmo markup do header, foco com `focus/ring-inverse`), o aviso **"Ateliê Bruma é uma marca fictícia criada para um piloto de avaliação. Todos os dados desta página são exemplos."** em `text/inverse-secondary` (stone-300, C12b), e o link "Voltar ao início" (§5.4, versão clara). Sem links externos, sem direitos/ano.

### 5.10 Seção alvo de âncora

O título da seção (`h2`) não fica coberto pelo header: `scroll-margin-top: 5rem`. Ao chegar por âncora, o `h2` recebe foco programático (`tabindex="-1"`). Se o navegador desenhar o anel de foco nele, ele usa o mesmo estilo do §2 e não pode ser cortado nem ficar sob o header (WCAG 2.4.11). Alvo `#colecao`: o `h2` "Coleção Névoa".

## 6. Layouts por seção e breakpoint

Larguras de conteúdo calculadas de `--gutter: clamp(1rem, 5vw, 2rem)` e contêiner de 72rem (1152 px, com padding): **320 → 288 px; 375 → 337,5; 768 → 704; 1024 → 960; 1440 → 1088** (margens laterais de 144 px). Tudo abaixo é **projeto**; alturas e quebras são estimadas e precisam de medição. Breakpoints: 360 (nav compacta), 768 (2 colunas), 1024 (3 colunas, respiro maior), 1440 (largura máxima atingida).

Respiro vertical entre seções: 64 px (<1024), 112 px (≥1024). Faixas: Hero e Coleção e Contato em `canvas`; Manifesto e Material em `surface`; Rodapé em `inverse`.

### 6.1 Header

| | 320 | 375 | 768 | 1024 | 1440 |
|---|---|---|---|---|---|
| Padding lateral | 12 | 18,75 | 32 | 32 | 32 (contêiner 1152; marca e nav alinhadas às margens do conteúdo) |
| Marca | 89 × 44 (logo 81 × 32) | idem | idem | idem | idem |
| Nav | 13 px/600, padding 4 | 14 px/500, padding 8 | 16 px/500, padding 14 | idem | idem |
| Observação | folga estimada ~17 px (§5.1) | ~18 px | espaço sobra | | |

### 6.2 Hero `#proposta`

| | 320 | 375 | 768 | 1024 | 1440 |
|---|---|---|---|---|---|
| Colunas | 1 | 1 | 2 (7fr / 5fr, gap 32) | 2 (7fr / 5fr, gap 48) | 2 (7fr / 5fr, gap 64) |
| Ordem | etiqueta, h1, subtítulo, apoio, **CTA**, imagem | idem | texto à esquerda, arco à direita, centrados na vertical | idem | idem |
| h1 | 36 px, 2 a 3 linhas (`text-wrap: balance`) | 36 px, 2 linhas | ~47 px | ~55 px | 64 px |
| CTA | largura total (máx. 22rem) | idem | automática | automática | automática |
| Imagem (arco 4:5) | 288 × 360, abaixo do CTA | 337 × 421 | ~280 × 350 | ~380 × 475 | ~427 × 534 (máx. 28rem = 448) |
| Primeira tela | h1, subtítulo e CTA visíveis em 375 × 667: soma estimada ~440 px, folga ~225. A 320 × 568: ~540 px, **folga ~28 px, apertado** (A CONFIRMAR) | | | | |

Padding vertical do hero: 32 px acima do conteúdo (celular), 64 px a partir de 1024. A etiqueta "Marca fictícia · página demonstrativa" fica acima do h1 e deve estar visível na primeira tela.

### 6.3 Manifesto `#manifesto`

| | 320 e 375 | 768 | 1024 | 1440 |
|---|---|---|---|---|
| Fundo | faixa `surface` | idem | idem | idem |
| Estrutura | 1 coluna: h2, introdução, lista de 3 afirmações | 1 coluna, medida 62ch | 2 colunas (5fr / 7fr, gap 64): à esquerda h2 e intro; à direita as 3 afirmações | idem, gap 96 |
| Afirmações | título em Fraunces 22 px (h3) + frase; filete `border/default` entre itens; sem ícones, sem numerais | idem | idem | idem |

### 6.4 Coleção `#colecao`

| | 320 | 375 | 768 | 1024 | 1440 |
|---|---|---|---|---|---|
| Cabeçalho | h2, intro, etiqueta, em 1 coluna | idem | h2 e intro à esquerda (medida 62ch), etiqueta abaixo | idem | idem |
| Grade de peças | 1 coluna, gap 40 | 1 coluna | **2 colunas**, gap 32 | **3 colunas**, gap 40 | 3 colunas, gap 40 |
| Largura de cada cartão | 288 | 337 | 336 | ~293 | ~336 |
| Altura estimada do placeholder (4:5) | 360 | 421 | 420 | 367 | 420 |
| Ideia de presente | texto com régua lateral 3 px em `clay-700` (decorativa), `padding-left: 16px`, **sem botão, sem link** | idem | idem | faixa de texto de largura de leitura | idem |

Observação de risco: a 320 e 375, seis placeholders 4:5 empilhados fazem a coleção rolar muito. **HIPÓTESE** de mitigação não adotada: reduzir para 3:4 só no celular. Decidir após ver fotos reais ou render (já listado em `art-direction.md` §7).

### 6.5 Material `#material`

| | 320 e 375 | 768 | 1024 | 1440 |
|---|---|---|---|---|
| Fundo | faixa `surface` | idem | idem | idem |
| Estrutura | 4 blocos empilhados (h3 + texto), etiqueta "Informações de exemplo" abaixo do h2 | **2 × 2**, gap 32 | 2 × 2, gap 48 | 2 × 2, gap 64 |
| Lista "Como cuidar" | lista simples com marcadores; **sem ícones** | idem | idem | idem |

### 6.6 Contato `#contato`

| | 320 e 375 | 768 | 1024 | 1440 |
|---|---|---|---|---|
| Estrutura | h2, etiqueta, `dl` empilhada (dt sobre dd) | `dl` com `11rem 1fr` | idem, largura máx. 40rem, à esquerda; coluna direita vazia (respiro) | idem |
| E-mail | em destaque, Figtree 500, 18 px, sublinhado; `overflow-wrap: anywhere` (endereço de 27 caracteres cabe em 288 px a 18 px, estimado ~245 px) | | | |

### 6.7 Rodapé

| | 320 e 375 | 768 e acima |
|---|---|---|
| Estrutura | marca, aviso, link "Voltar ao início", empilhados à esquerda | marca à esquerda; aviso e link em coluna à direita, ou empilhados (decisão do Developer; sem mudança de conteúdo) |

### 6.8 Zoom e reflow

Zoom 200% a 320 de largura efetiva (viewport de 640 px a 200%) e 400% a 1280 px: layout de 320 px. Sem rolagem horizontal. Header com `flex-wrap`. Texto em `rem`. Espaçamento de texto ajustável (WCAG 1.4.12) sem cortes: nenhuma caixa de texto com altura fixa (o placeholder tem `aspect-ratio`, mas a legenda e o alt estão em caixas que crescem com o conteúdo; a 400% o `alt` visível pode cobrir boa parte do placeholder, **A CONFIRMAR**).

## 7. Tabela de contrastes

**Como foram calculados e conferidos:** este agente calculou **à mão**, pela fórmula WCAG 2.x (luminância relativa com linearização sRGB; razão (L1 + 0,05) / (L2 + 0,05)), e **não rodou script nem verificador**. A **revisão independente conferiu por script** (`evidence/UI-001/contrast-check.json`): os 20 pares desta tabela conferem, diferença máxima 0,04 (C15: 9,70 declarado, 9,66 medido). Onde o script mediu um valor ligeiramente diferente (C8, C14, C15), a tabela traz o valor do script. C11, C12 e C16 não têm entrada própria no script depois da troca da borda; seus valores vêm dos pares idênticos C2, C3b e C3, e C16b do par `C16b-fix` (ink-700 / mist-300 = 4,43). Isso confere **razões de contraste**, não conformidade WCAG. Mínimos: texto normal 4,5; texto grande (≥ 24 px ou ≥ 18,66 px em negrito) e componentes/foco 3.

| ID | Primeiro plano / fundo (hex) | Uso | Razão | Mínimo | Resultado (conferido por script) |
|---|---|---|---|---|---|
| C1 | ink-900 `#25231F` / fog-50 `#F4F1EC` | texto principal, links do header, mono claro, anel de foco | 13,92 | 4,5 | passa |
| C1b | ink-900 / fog-100 `#EAE6DF` | texto em faixa, anel de foco em surface | 12,61 | 4,5 | passa |
| C1c | ink-900 / fog-200 `#D9D4CB` | texto da etiqueta, logo em hover/ativo | 10,63 | 4,5 | passa |
| C2 | ink-700 `#55514A` / fog-50 | texto secundário, medida, legenda | 7,00 | 4,5 | passa |
| C3 | ink-700 / fog-200 | borda da etiqueta (componente) | 5,35 | 3 | passa |
| C3b | ink-700 / fog-100 | texto secundário em faixa | 6,34 | 4,5 | passa |
| C4 | clay-700 `#8A3F22` / fog-50 | link, símbolo/faixas do logo, limite do CTA | 6,62 | 4,5 (texto), 3 (gráfico) | passa |
| C5 | clay-700 / fog-100 | link em faixa | 6,00 | 4,5 | passa |
| C5b | clay-700 / fog-200 | faixas do logo em estado ativo | 5,06 | 3 | passa |
| C6 | fog-50 / clay-700 | texto do CTA, padrão | 6,62 | 4,5 | passa |
| C7 | fog-50 / clay-800 `#6F3019` | CTA hover; link hover em canvas | 8,82 | 4,5 | passa |
| C8 | fog-50 / clay-900 `#5A2813` | CTA ativo; link ativo em canvas | 10,67 | 4,5 | passa |
| C9 | ink-700 / fog-50 | borda tracejada da etiqueta vs. página | 7,00 | 3 | passa |
| C10 | fog-50 / ink-900 | rodapé, skip link, mono escuro | 13,92 | 4,5 | passa |
| C11 | ink-700 `#55514A` / fog-50 | borda do placeholder vs. página | 7,00 | 3 | passa |
| C12 | ink-700 / fog-100 | borda do placeholder em faixa | 6,34 | 3 | passa |
| C12b | stone-300 `#BDB7AC` / ink-900 | aviso do rodapé | 7,87 | 4,5 | passa |
| C13 | ink-900 / fog-50 | anel de foco (3 px) sobre canvas | 13,92 | 3 | passa |
| C13b | fog-50 / ink-900 | anel de foco no rodapé | 13,92 | 3 | passa |
| C14 | clay-800 / fog-100 | link hover em faixa | 7,99 | 4,5 | passa |
| C15 | clay-900 / fog-100 | link ativo em faixa | 9,66 | 4,5 | passa |
| C16 | ink-700 / fog-200 | borda do placeholder vs. fim do degradê | 5,35 | 3 | passa |
| C16b | ink-700 / mist-300 `#B9C4C8` | borda do placeholder vs. pior caso do gradiente | **4,43** | 3 | **passa** (resolvido na rodada 3; era 2,56 com stone-500, falha confirmada pelo script) |

Histórico C11/C12/C16/C16b com a borda stone-500 (rodada 2, **descartada**): 4,05 · 3,67 · 3,09 · 2,56 (os quatro conferidos pelo script; só o último falhava).

**Não dependem de cor sozinha:** links (sublinhado), hover do header (sublinhado), etiqueta (texto + tracejado), foco (contorno), faixas do logotipo (interrupções geométricas, legíveis em uma cor).

**Combinações proibidas** (não calculadas ou reprovadas): texto sobre `mist-300`/gradiente; texto stone-300 sobre fundo claro; qualquer uso de stone-500 (retirado); `border/default` (fog-200) como única marca de um controle; clay-700 sobre ink-900.

**Logotipo:** C1, C1b, C1c, C4, C5, C5b, C10 cobrem todos os usos (README do logotipo §4.2).

## 8. Lista de assets e licenças

| Asset | Origem | Licença | Situação |
|---|---|---|---|
| Logotipo (5 SVGs) | Criação original desta tarefa; letras como paths próprios, sem `<text>`, sem fonte embutida | Titularidade **não definida** (pergunta ao proprietário). FICTÍCIO, não aprovado | Entregue em `docs/ui/logo/` |
| Fraunces (variável, WOFF2 a gerar) | <https://github.com/undercasetype/Fraunces> (também <https://github.com/google/fonts/tree/main/ofl/fraunces>) | SIL Open Font License 1.1, <https://openfontlicense.org/> (arquivo `OFL.txt` do repositório) | **Não baixada nem verificada nesta sessão.** Developer baixa, arquiva `OFL.txt` e confere o campo de "Reserved Font Name": subsetar/converter pode contar como versão modificada e exigir outro nome; usar os arquivos distribuídos sem alteração se houver dúvida |
| Figtree (variável, WOFF2 a gerar) | <https://github.com/erikdkennedy/figtree> (também <https://github.com/google/fonts/tree/main/ofl/figtree>) | SIL Open Font License 1.1 | Idem |
| Fontes de fallback | Fontes do sistema do visitante (Iowan Old Style, Palatino Linotype, Georgia, system-ui, Segoe UI, Roboto) | Não distribuídas por este projeto | Nenhuma ação |
| Fotografias | **Nenhuma.** `assets_approved: false` | n/a | Hero e 6 peças são placeholders |
| Ícones | **Nenhum** pacote. Nenhum glifo (nem seta) | n/a | Qualquer glifo futuro deve ser CSS/SVG próprio e documentado |
| Imagem social (Open Graph) | **Nenhuma** (`content-structure.md` §0) | n/a | n/a |
| Gradiente de névoa | CSS puro (cores do próprio projeto) | n/a | Decoração |
| Biblioteca Figma EIXO / tokens EIXO | **Não usados**; sem identidade EIXO | n/a | n/a |

Fontes: auto-hospedar em WOFF2, subconjunto latino com acentos de português, `font-display: swap`, métricas de fallback ajustadas (`size-adjust`) para limitar CLS. Até o `OFL.txt` estar arquivado, usar só as pilhas de fallback.

## 9. O que não foi verificado

- **Avaliação visual: ninguém a fez.** Este agente não renderizou nada. A revisão independente renderizou `preview.html` (Playwright + Chromium headless, `render-check.json`) e mediu rolagem, header a 320 px e carregamento dos SVGs, mas **não registrou julgamento visual**. Seguem sem avaliação visual: o **novo desenho do símbolo** (proporção do gargalo, leitura como vaso, afinamento do traço a 32 px), o encaixe das letras e o aspecto da borda de placeholder em ink-700.
- **Rolagem horizontal da prancha:** corrigida por análise de CSS (§0), **sem nova medição**.
- **Header a 320 px:** medido em uma linha (308 de 320 px) com fonte de fallback; **com Figtree real a largura pode mudar** e a medição deve ser repetida quando a fonte for embutida.
- Razões de contraste: calculadas à mão e conferidas por script pela revisão (§7); C16b resolvido com ink-700 (4,43). Isso não é conformidade WCAG.
- Quebras de linha do h1, alturas de seção e folga da primeira tela (375 × 667 e 320 × 568): estimativas.
- Fontes: URLs, licenças, "Reserved Font Name", presença dos eixos `opsz`/`SOFT`/`WONK` do Fraunces e sua exposição nos arquivos usados: **não verificados**. Os valores de `font-variation-settings` são decisão do Developer após conferir o arquivo real.
- Leitor de tela (nome do link da marca, anúncio da lista de 6 itens, `role="img"` nos placeholders), navegação por teclado, WCAG 2.2 AA integral: não testados. Contraste e esta especificação **não** equivalem a conformidade WCAG.
- Estado "imagem falhou" do logotipo (`<img>` com `alt` e `width`/`height`) varia entre navegadores: não testado.
- Tema escuro: **não projetado** (`color-scheme: light`); não há aliases escuros além do rodapé.
- Anterioridade/marca registrada do logotipo: não pesquisada (marca fictícia).
- Reconhecimento do símbolo como "vaso de cerâmica" por pessoas: não testado (HIPÓTESE).
- Pesquisa de mercado: usada como FATO onde citada (público de 25 a 44 anos, decisão 55% emocional, barreira de qualidade 39% e preço 27%, Pesquisa §1.1 e §2.1) e como HIPÓTESE onde a UI extrapola (calma = adequado ao público; CTA largo no celular; placeholders tracejados como linguagem). Nenhuma foi testada.
- Sites de referência da pesquisa: **não inspecionados** (`art-direction.md` §2).

## 10. Mapeamento para o Developer (resumo)

- Importar `tokens.css` (ou gerar a partir de `tokens.json`; se gerar, a sincronia deixa de ser manual).
- Marcação do header e dos cartões: §5 e `content-structure.md`. Copy: `content-structure.md` (qualquer mudança volta ao UX).
- Componentes não interativos (cartão, etiqueta, placeholder) não podem ganhar hover nem cursor de ação.
- Critérios a atender nos testes: `docs/ux/acceptance-criteria.md` (M1 a M12, WCAG 2.2 AA aplicável).
- Registro das exceções: **nenhuma exceção de contraste** (C16b resolvido na rodada 3 com `border/strong` = ink-700; `stone-500` não existe mais nos tokens, não reintroduzir). Pendentes: nav a 320 px com a fonte real (medida só com fallback), primeira tela a 320 × 568 (estimativa).

## 11. Perguntas para o proprietário

1. **Direção:** aprova "Névoa quieta" (A) ou quer ver a "Esmalte" (B) desenvolvida? A recusa de B foi decisão de projeto, não prova.
2. **Símbolo:** o vaso redesenhado (lábio, gargalo curto, ombro, base plana) resolve a leitura de "frasco de laboratório" que o revisor apontou, ou prefere outro objeto (caneca, tigela)? A caneca é a peça de maior apelo de presente (Pesquisa §3.2, FICTÍCIO).
3. **Faixas de bruma no símbolo:** aceita mantê-las dentro do contorno, sabendo que podem lembrar graduação de recipiente de medida? Alternativa: só no ícone.
4. **Titularidade do logotipo fictício:** deve ser registrada (ex.: `LICENSE` do repositório)? Hoje está indefinida.
5. **Tracejado como identidade:** aceita que etiquetas e placeholders tenham traço tracejado como marca visual de "fictício/ilustrativo", mesmo com o risco de parecer componente quebrado?
6. **Fotos:** haverá fotos próprias ou licenciadas por escrito? Até lá, `assets_approved` fica `false` e a página mostra placeholders.
7. **Fontes:** autoriza o Developer a baixar Fraunces e Figtree e arquivar as licenças OFL no repositório?
8. ~~Borda do placeholder (C16b)~~ **Resolvida por padrão na rodada 3:** a borda é `ink-700` (4,43 no pior caso, medido pela revisão). Reversível pelo proprietário: se preferir uma borda mais suave, é preciso um tom com pelo menos 3:1 sobre `mist-300` (#B9C4C8), o que na prática aproxima de ink-700; a alternativa é remover o `mist-300` do gradiente.
9. **Render e medição:** a revisão independente já rodou contraste por script e renderizou a prancha (mediu, não avaliou visualmente). Falta: nova medição da rolagem após a correção da rodada 3, e **olhar** a prancha e o símbolo. Quem fará a avaliação visual?

## 12. Estado de transferência

UI-001 está **pronta para revisão** (`READY_FOR_REVIEW`), não concluída: sem Figma, sem avaliação visual por ninguém, sem nova medição da correção de rolagem (rodada 3), sem aprovação humana. Contraste conferido por script pela revisão independente. O registro em `handoffs/state.json` é do Orchestrator; este agente não o alterou.


## 13. Decisões do proprietário (2026-10-22T10:23:04Z)
Resposta literal: "Sim para as 3 perguntas", às perguntas 1 a 3 do resumo da PR #6:
1. Direção "Névoa quieta" e logotipo: **aprovados**.
2. Faixas de bruma dentro do símbolo: **mantidas**.
3. Tracejado como marca visual de "fictício/ilustrativo": **aceito**.

Perguntas 4 (titularidade do logotipo fictício), 6 (fotos) e 7 (licenças OFL das fontes) seguem abertas e passam para DEV-001 com padrão razoável: titularidade indefinida, placeholders no lugar de fotos e licenças OFL arquivadas pelo Developer ao embutir as fontes.
