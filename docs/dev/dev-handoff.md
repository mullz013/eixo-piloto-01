# Handoff Developer → QA / Quality: Ateliê Bruma (DEV-001)

**Projeto:** piloto-01 · **Task:** DEV-001 · **Agente:** eixo-fullstack-developer · **DNA:** v0.2.0 (briefing FICTÍCIO) · **Entradas:** UX-001 e UI-001 (aprovados, `handoffs/approval-log.md`)
**Status proposto:** `READY_FOR_QA` (não é GO, não é release). Deploy continua proibido. `handoffs/state.json` não foi alterado (é do Orchestrator). Nada foi commitado nem enviado.

## 0. O que foi e o que não foi feito (leia primeiro)

| Item | Situação |
|---|---|
| Implementação | **IMPLEMENTED** (arquivos abaixo). |
| Render, medição, screenshots, axe, Lighthouse, validação HTML, testes | **NOT_RUN.** Este agente não renderizou nada, não mediu nada, não rodou nenhum teste. Tudo o que está descrito como "layout", "largura" ou "folga" abaixo vem de leitura da especificação e do CSS, não de observação. |
| Cópia de `tokens.css` e dos SVGs | O shell exigiu aprovação e não foi concedido. Os 4 arquivos foram **recriados com Write a partir do texto lido** (não com `cp`). **Igualdade byte a byte NÃO verificada** (`cmp`/`diff` não rodou). **QA deve rodar `diff docs/ui/tokens.css site/tokens.css` e `diff docs/ui/logo/<arquivo>.svg site/assets/<arquivo>.svg`.** Os valores de cada token foram transcritos sem alteração, mas isso é uma afirmação do autor, não uma checagem. |
| Fontes | `site/fonts/` não foi tocada. Que o `@font-face` carregue os WOFF2 e que os eixos `opsz`/`wght` funcionem é **não verificado**. |
| Figma | Não existe (UI-001 entregue em arquivos). Não há frame de comparação. |

## 1. Arquivos entregues

| Arquivo | Conteúdo |
|---|---|
| `site/index.html` | Página única, `lang="pt-BR"`, `<title>`, meta description, `noindex`, favicon, skip link, header, 5 seções, rodapé. Sem `<script>`, sem `<form>`, sem recurso externo. |
| `site/styles.css` | `@font-face` (swap + fallbacks com `size-adjust`), base, header, componentes, seções, rodapé. |
| `site/tokens.css` | Cópia de `docs/ui/tokens.css` (ver §0 sobre verificação). |
| `site/assets/logo-principal.svg` | Header. |
| `site/assets/logo-mono-fundo-escuro.svg` | Rodapé. |
| `site/assets/icone.svg` | Favicon (`<link rel="icon" type="image/svg+xml">`). |
| `docs/dev/adr-001-stack.md` | ADR curta. |
| `docs/dev/dev-handoff.md` | Este arquivo. |

Não copiados por não terem uso: `logo-mono-fundo-claro.svg`, `icone-fundo-escuro.svg`.

## 2. Mapeamento handoff → código

| Requisito (`ui-handoff.md` / UX) | Onde está |
|---|---|
| §3 estrutura e ids | `body#topo` → `.skip` → `header` → `main#conteudo[tabindex=-1]` com `#proposta`, `#manifesto`, `#colecao`, `#material`, `#contato` → `footer`. Cada `section` com `aria-labelledby` (`t-proposta`, `t-manifesto`, `t-colecao`, `t-material`, `t-contato`). |
| §3 `scroll-padding-top` / `scroll-margin-top` | `styles.css`: `html{scroll-padding-top:var(--anchor-offset)}` e `:where([id]){scroll-margin-top:var(--anchor-offset)}`. Rolagem suave só em `@media (prefers-reduced-motion: no-preference)`. |
| §5.1 header | `.site-header` (sticky, `top:0`, fundo canvas opaco, filete 1 px), `.site-header__in` (flex, `flex-wrap:wrap`, `justify-content:space-between`, gap 8 px / 12 px a partir de 360). Padding lateral 12 px abaixo de 360, `--gutter` depois. Marca 81 × 32 em px, alvo ≥ 44. Nav: 13/600 e padding 4 (<360), 14/500 e 8 (360–767), 16/500 e 14 (≥768). Estados hover/ativo/foco da marca e dos links. Nome acessível: `<img alt="Ateliê Bruma">` + `<span class="sr-only">, início</span>`. |
| §5.2 skip link | `.skip`: `position:fixed`, `transform:translateY(-200%)` até receber foco; fundo inverse, texto inverse, z-index 1000 (acima do header, z-index 100). |
| §5.3 CTA | `.btn` em `<a href="#colecao">`: pílula, `min-height:52px`, padding 28 px, 17 px/600; hover clay-800, ativo clay-900; abaixo de 480 px `width:100%; max-width:22rem`. Único elemento com aparência de botão. |
| §5.4 links de texto | `.link` (clay-700, sublinhado 2 px, offset 3 px, `min-height:44px`); hover clay-800 e 3 px; ativo clay-900; variante `.link--inverse` no rodapé com `focus-ring-inverse`. E-mail: `mailto:` com o endereço como texto, `.link--mail` 18 px, `overflow-wrap:anywhere`. |
| §5.5 cartão | `li.piece` em `ul.pieces[role=list]`: filete superior 1 px ink-900, ordem placeholder → h3 → medida → preço → frase. Sem hover, sem cursor de ação. Preço `R$ N (exemplo)` com `.ex`. |
| §5.6 placeholder | `figure.ph-fig` > `div.ph[role=img][aria-label=alt aprovado]` + `figcaption.ph__cap`. `aspect-ratio:4/5`, borda 2 px tracejada `--border-strong`, gradiente de névoa (fallback sem `color-mix` na primeira declaração), raio 20; hero com `--radius-arch` e `max-width:28rem`. Legenda em caixa sólida canvas, canto inferior esquerdo, sem regra que a oculte. |
| §5.7 etiqueta | `.tag`: raio 4, fundo chip, borda 2 px tracejada ink-700, 13/600, `padding:3px 8px`, pode quebrar linha. Textos de `content-structure.md`. |
| §5.8 contato | `dl.dl` com linhas `div > dt + dd`; `dt` 14/600 secundário; ≥768 grid `11rem 1fr`; largura máx. 40rem. Endereço em texto simples. |
| §5.9 rodapé | `.site-footer`: fundo inverse, marca mono escura (link `#topo`), aviso em stone-300, "Voltar ao início". Decisão do Developer (§6.7): ≥768 px marca à esquerda, texto e link à direita. |
| §5.10 / UX §6.2 foco em âncora | `tabindex="-1"` nos `h2`/`h1` e nas `section` (ver desvio D1). |
| §6.2 a §6.6 layouts | Hero 1 col → 7fr/5fr a partir de 768 (gap 32/48/64 em 768/1024/1440); Manifesto 1 col → 5fr/7fr a partir de 1024 (gap 64/96); Coleção 1/2/3 colunas (768/1024); Material 1 col → 2 × 2 a partir de 768; Contato `dl`. Respiro `--section-y` (64/112). |
| §4 proibições | Sem JS, form, depoimentos, selos, segundo CTA, ícones, imagens de banco, recurso externo. |
| Tokens | Todas as cores vêm de variáveis de `tokens.css`; nenhum hex literal em `styles.css`. |

## 3. Desvios e perguntas abertas

| ID | Tipo | Descrição |
|---|---|---|
| D1 | Desvio técnico | O handoff pede `tabindex="-1"` nos títulos. Como os **ids de âncora estão nas `section`**, o navegador foca o elemento que tem o id; por isso `tabindex="-1"` também foi posto nas `section` e em `main`. Para não desenhar o anel de foco no bloco inteiro, `main:focus, section:focus{outline:none}`. Os controles reais (links, CTA, e-mail) e os títulos mantêm o anel. **Pergunta:** o UI aceita o anel suprimido em contêineres focados só por programa? Impacto em WCAG 2.4.7 é de revisão manual (QA/Quality). |
| D2 | Copy | `content-structure.md` §6 traz "Encomendas: prazo de até 45 dias." em minúscula depois do rótulo. Foi usado "Prazo de até 45 dias." (maiúscula), como em `preview.html`, porque o `dd` começa a frase. Única alteração de copy. |
| D3 | Copy opcional | Incluídas as duas linhas marcadas como opcionais: "“Bruma” é névoa: tons suaves, bordas que se diluem." (Manifesto) e "Escreva para saber quais peças da fornada estão disponíveis." (Contato). Sem prazo prometido. Se o UX preferir omitir, são duas linhas a remover. |
| D4 | Ambiguidade UI | `ui-handoff.md` §5.6 diz "Imagem falhou (e também modo padrão sem arquivo)" com o `alt` visível em caixa, mas a prancha mostra o placeholder padrão só com a legenda. Foi seguida a prancha: **o alt fica em `aria-label`, não visível**, nos 7 placeholders. Como os placeholders são CSS e não há arquivos de imagem, o estado "imagem falhou" **não existe** hoje nas peças (só no logotipo, que é `<img>`). **Pergunta:** o alt deve ficar visível também no padrão? |
| D5 | Estimativa | `size-adjust` dos fallbacks (Fraunces→Georgia 98%, Figtree→Arial 100%) são estimativas, sem `ascent-override`/`descent-override`. A medição de CLS pode pedir ajuste. |
| D6 | Adição | `<meta name="color-scheme" content="light">`, `:root{color-scheme:light}` e `<meta name="format-detection" content="telephone=no, address=no, email=no">` (evita que navegadores móveis transformem o endereço fictício em link/mapa; AC-CON-03/08). |
| D7 | Detalhe não especificado | Hover/ativo da marca no rodapé usa `color-mix()` de fog-50 a 12%/20%. A UI não especifica. |
| D8 | Detalhe não especificado | Hero: padding superior de 32 px no celular e 64 px a partir de 1024; inferior `--section-y`. Etiqueta do "R$ 182 (exemplo)" do presente aplicada com `.ex` dentro do `<strong>`. |
| D9 | Título | `<title>` com "Ateliê Bruma | Cerâmica de mesa feita à mão (marca fictícia)", lendo o `|` do quadro de `content-structure.md` §0 como parte do texto. |

Nenhum conflito UX × UI exigiu escolher um lado além de D2 e D4.

## 4. O que NÃO foi verificado

- Tudo que depende de render: quebra de linha do h1, altura da primeira tela (AC-P0-01, M1), largura do header a 320 e 375 px **com Figtree real** (a UI mediu só com fallback), rolagem horizontal (M5), aspecto visual do placeholder em ink-700, fidelidade ao `preview.html`.
- Primeira tela a 320 × 568 foi estimada pela UI como apertada (folga ~28 px); não há medição. Nesta implementação o hero tem etiqueta + h1 + subtítulo + apoio + CTA antes da imagem, na ordem da UI.
- Carregamento real das fontes e dos SVGs (caminhos relativos `fonts/…`, `assets/…`).
- Suporte a `color-mix()`, `text-wrap: balance`, `:where()` em navegadores-alvo; os dois primeiros são melhoria progressiva (falham sem quebrar).
- Comportamento do foco programático ao ativar âncoras (D1), com teclado e leitor de tela.
- Contraste: cores e pares vêm de `tokens.css` já conferidos pela revisão da UI; não foram recalculados. Não há par novo além dos do §7 da UI, **exceto** o hover/ativo do rodapé (D7), não calculado.
- LCP/CLS/INP, axe, validação HTML, WCAG 2.2 AA: nada foi executado. Não se afirma conformidade WCAG.

## 5. Segurança e privacidade
Sem JavaScript, formulário, cookies, storage, analytics ou terceiros; sem segredos nem dados pessoais (e-mail e endereço são fictícios, `.example`). Nenhum cabeçalho HTTP, CSP ou deploy foi configurado (ADR-001). `noindex` presente na página.

## 6. Checklist de reteste para QA (IDs de `docs/ux/acceptance-criteria.md`)

Todas as linhas estão **NOT_RUN** pelo Developer. Viewports: 320 × 568, 375 × 667, 768 × 1024, 1024 × 768, 1440 × 900 e 667 × 375.

| ID | O que checar nesta implementação |
|---|---|
| AC-P0-01 / M1 | 375 × 667: h1, subtítulo e `.btn` inteiros sem rolar. Registrar também 320 × 568. |
| AC-P0-02 / M2 | Ativar `a.btn`: URL termina em `#colecao`; h2 "Coleção Névoa" visível sob o header; `document.activeElement` é a `section#colecao` (ou o h2). |
| AC-P0-03 / M4 | 6 `li.piece`, cada um com h3, medida, `R$ N (exemplo)` visíveis sem interação. |
| AC-P0-04 / M3 | De qualquer ponto, "Contato" no header leva a `#contato` com h2 e e-mail legíveis; 1 ativação. |
| AC-P0-05 | `#contato` mostra e-mail, cidade, feira, prazo e a etiqueta "Dados de exemplo…". |
| AC-NAV-01 | 1º Tab = "Pular para o conteúdo" visível; Enter foca `main#conteudo`. |
| AC-NAV-02 | Abrir `index.html#contato` e `#colecao`: título não fica sob o header. |
| AC-NAV-03 | Voltar do navegador após âncora. |
| AC-NAV-04 | Tab após âncora segue a partir da seção alvo (depende de D1). |
| AC-NAV-05 | JS desabilitado: tudo funciona (não há `<script>`). |
| AC-NAV-06 | `prefers-reduced-motion: reduce`: salto imediato; sem transições. |
| AC-NAV-07 | `#naoexiste` abre no topo sem erro. |
| AC-NAV-08 | "Voltar ao início" e logotipo do header levam a `#topo`. |
| AC-NAV-09 | Logo com 32 px de altura nos viewports de 320 e 375, link para `#topo`, nome acessível "Ateliê Bruma, início", foco visível, alvo ≥ 44, sem rolagem horizontal, 3 links visíveis (se a nav quebrar para a 2ª linha, registrar a altura do header e o efeito no `--anchor-offset`). |
| AC-CON-01 / M10 | Preços, medida técnica, 1.240 °C, prazos, feira, endereço, e-mail, cidade: etiqueta ou bloco rotulado. |
| AC-CON-02 / M11 | Nenhum depoimento, nota, estrela, selo, "mais vendido". |
| AC-CON-03 | Sem `<form>`, `wa.me`, `tel:`, CEP, mapa, rede social, script; único endereço é o fictício. |
| AC-CON-04 | 7 placeholders com legenda "Imagem ilustrativa (placeholder)" visível, `aria-label` conforme `content-structure.md`, proporção 4:5. Nenhum arquivo de imagem. |
| AC-CON-05 | Bloquear imagens: texto intacto, layout íntegro. Atenção ao logotipo (alt como texto, caixa 81 × 32). |
| AC-CON-06 | Endereço de e-mail visível e selecionável. |
| AC-CON-07 | Exatamente um elemento de ação primária. |
| AC-CON-08 | Endereço fictício em texto, sem link, com a etiqueta no mesmo bloco. Conferir que nenhum navegador móvel o linkifica. |
| M5 | Zero overflow horizontal de 320 a 1440 px; zoom 200% e 400%; espaçamento de texto aumentado. |
| M6 | Alvos ≥ 24 px (recomendado 44) no header, CTA e e-mail. |
| M7 | Contraste texto 4,5 / grande 3 / componentes e foco 3, incluindo estados hover/ativo/foco e o rodapé. |
| M8, M9 | LCP e CLS (Lighthouse, ≥ 3 execuções, versão registrada). Atenção ao CLS na troca de fonte (D5). |
| M12 | axe (ou equivalente) em 5 viewports; revisão manual por Quality. |
| Integridade | `diff` de `site/tokens.css` e dos 3 SVGs contra `docs/ui` (ver §0); `site/fonts/` inalterada. |

## 7. Crítica técnica (para o Orchestrator)
- **Reuso:** `tokens.css`, `.tag`, `.ph`, `.link` e `.btn` são genéricos; a estrutura de seções, a copy e o tracejado como marca são do cliente. Nada da identidade EIXO foi usado.
- **Dívida:** seis cartões repetidos à mão; fallbacks de fonte estimados; foco em contêineres (D1); sem teste automatizado no repositório.
- **Testes que deveriam entrar na suíte:** os de AC-P0/NAV/CON por Playwright, varredura de proibidos (AC-CON-03) e `diff` de tokens como verificação de CI.
- **Próximo responsável:** QA Engineer e Quality Specialist em paralelo; a sessão coordenadora faz primeiro o render/medição pedido.
