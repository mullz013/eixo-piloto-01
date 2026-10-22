# Revisão UI-003: padrões do moodboard aplicados à loja

**Projeto:** piloto-01 · **Task:** UI-003 · **Agente:** eixo-ui-art-director · **Data:** 2026-10-22 · **Entrada:** `moodboard-002.md` (P1 a P10; imagens não lidas, só a descrição), `revisao-002.md`, `art-direction.md` §1 a §3, `site/tokens.css`, `site/styles.css`, `site/index.html`
**Status:** PROPOSTA, aguarda aprovação humana antes do Developer. Nada foi renderizado, nem no Figma (MCP não conectado) nem no navegador: medidas são de projeto, não de captura.

## 0. O que não muda (decisões de e-commerce, intactas)

Carrossel 4 por vez no desktop e 2 + corte no celular (`--card-w`); hambúrguer abaixo de 1024 px; 5 categorias com filtro; coleções passadas (Terra Molhada, Sal); faixa de vantagens logo abaixo do banner; sacola em gaveta, barra de frete, botão "Pausar animação" (WCAG 2.2.2); ordem e ids das seções. Muda só a **pele**: raio, superfície, tipografia de destaque, cartões. Argila `#8A3F22` segue como única cor de ação (botões, contador, barra de frete, ícones de vantagem).

## 1. Tokens novos (adicionar a `tokens.css`; nenhum valor existente muda)

| Token | Valor | Uso |
|---|---|---|
| `--radius-card` | 20 px | cartões de categoria, FAQ, cartões flutuantes, imagem do produto no desktop |
| `--radius-card-sm` | 16 px | imagem do produto no celular |
| `--radius-panel` | 28 px (< 1024) · 32 px (≥ 1024) | hero, "O ateliê", rodapé |
| `--radius-panel-sm` | 24 px (< 1024) · 28 px (≥ 1024) | faixa de vantagens |
| `--shadow-float` | `0 18px 40px -16px rgb(37 35 31 / .28), 0 2px 6px rgb(37 35 31 / .06)` | **só** os 2 cartões do hero |
| `--shadow-lift` | `0 12px 24px -14px rgb(37 35 31 / .30)` | hover de categoria e de imagem de produto |
| `--glass` | `rgb(248 245 240 / .86)` + `backdrop-filter: blur(14px)`; fallback sólido `#F8F5F0` | cartões flutuantes |
| `--panel-gap` | `var(--gutter)` (18,75 px a 375; 32 px a 1440) | margem lateral e entre painéis |

Exceção a registrar: UI-001 §5.5 dizia "sem sombras". A sombra passa a existir apenas onde algo **flutua** sobre imagem; fora do hero, o resto continua plano.

## 2. Tipografia de destaque (P1)

`@font-face` novo: `Fraunces`, `font-style: italic`, `font-weight: 300 600`, `src: fonts/fraunces-italic-latin-var.woff2`, `font-display: swap`. Pré-carregar só esse arquivo (aparece na primeira dobra, no h1). Definir `font-synthesis: none` para nunca haver itálico falso.

Regra `.sec__title em, .hero__title em`: `font-style: italic; font-variation-settings: "opsz" 96 (144 no h1), "WONK" 1, "SOFT" 0; font-weight: 300; color: var(--clay-700); letter-spacing: inherit`. Sem sublinhado, nunca dentro de link.

| Título | Marcação | Tamanho 375 → 1440 |
|---|---|---|
| H1 hero | A névoa *virou mesa.* | 54,5 px → 108 px (já é `clamp(3rem, 2rem + 6vw, 6.75rem)`) |
| Novidades da *fornada* · Compre por *categoria* · Coleções *passadas* | `em` na palavra final | 29 px → 40 px (já é `--size-h2`) |
| O ateliê (fundo escuro) | Uma ceramista, um forno, *uma fornada por mês.* | 29 px → 40 px; itálico em **argila clara `#EFD9CC`** (11,55:1 sobre `#25231F`); argila `#8A3F22` ali daria 2,10:1 (cálculo manual: `(0,1408)/(0,0669)`) |
| Ajuda | sem itálico (copy não pede destaque) | igual ao atual |

Decisão para o proprietário: o P1 pede argila no itálico, mas `art-direction.md` §5.2 diz "nada decorativo em argila". Recomendo seguir o moodboard (argila `#8A3F22` sobre `#F4F1EC` dá 6,62:1, cálculo manual; não sublinhado para não parecer link). **Plano B:** itálico em `#55514A`, sem perder a forma.

## 3. Pastéis das categorias (P5) e contraste, **cálculo manual**

Contraste calculado **à mão com a fórmula WCAG 2.x** (luminância relativa `0,2126R + 0,7152G + 0,0722B` com linearização sRGB; razão `(L1+0,05)/(L2+0,05)`), por este agente, sem ferramenta de auditoria e **sem conferência por script nem por revisão independente**. Referência: `L(#25231F)` = 0,0169; `L(#55514A)` = 0,0830. Arredondado a 2 casas.

| Categoria | Pastel | Origem | L | `#25231F` | `#55514A` |
|---|---|---|---:|---:|---:|
| Canecas e xícaras | Névoa `#E6E7E3` | igual a `--tint-nevoa` | 0,795 | 12,62:1 | 6,35:1 |
| Pratos | Sal `#E1E7E8` | igual a `--tint-sal` | 0,789 | 12,54:1 | 6,31:1 |
| Tigelas | Areia `#EDE3D7` | igual a `--tint-terra` | 0,778 | 12,37:1 | 6,23:1 |
| Travessas | Musgo claro `#E1E6D8` | **novo**; matiz esverdeado ajustado a mão a partir de `mist-300`/`stone-300` | 0,775 | 12,33:1 | 6,20:1 |
| Vasos e jarras | Argila clara `#EFD9CC` | **novo**; matiz de `clay-700` clareado a mão (não é mistura linear) | 0,723 | 11,55:1 | 5,81:1 |

Todos acima de 4,5:1 nos dois textos (nome 14 px/600 em `#25231F`, contagem 13 px em `#55514A`). Os pastéis são **decorativos**: nenhum é cor de ação, e o limite do cartão não carrega informação (o texto identifica). Contra o canvas `#F4F1EC` (L 0,882) a razão é de cerca de 1,1 a 1,2:1; por isso o cartão não depende da borda. Fora das categorias, os mesmos Névoa/Areia/Sal seguem como fundo de imagem de produto.

## 4. Componentes

Larguras: 375 → painel útil 337,5 px (gutter 18,75); 1440 → container 1280, painel 1216 px. 768 a 1023 usa os valores de 375 com padding interno de 40 px (não detalhado).

### 4.1 Hero em painel (P2, P6)

| | 375 | 1440 |
|---|---|---|
| Painel | largura 337,5; margem superior 12; raio 28 | largura 1216; margem superior 16; raio 32; altura `clamp(600, 100svh − 108, 780)` (já existe) |
| Cena | altura `clamp(340, 92vw, 460)` = 345, no topo do painel | coluna direita, `inset: 0 0 0 42%` |
| Texto | abaixo da cena; padding 28 24 32; botão em largura total | coluna esquerda, centralizada na vertical, `max-width` 36rem; padding-left 64 |
| Kicker em pílula (P6) | altura 32; padding 0 14; raio 999; fundo `#F4F1EC`; borda 1 `rgb(37 35 31 / .16)`; Figtree 13/600, caixa-alta, 0,14em, `#55514A` (7,00:1 sobre fog-50, cálculo manual) | idem |
| Fundo | gradiente atual da cena (inalterado), recortado pelo raio via `overflow: hidden` | idem |

Estados: o painel não é clicável. Botão "Comprar a coleção" e link "Ver categorias" mantêm hover/ativo/foco atuais (foco 3 px `#25231F`, offset 3; como o painel recorta, o anel de foco do botão fica dentro dele, com margem ≥ 24 px). Celular: o botão "Pausar animação" fica no canto superior esquerdo a 12 px das bordas.

### 4.2 Cartões flutuantes do hero (P3)

Sem nota, avaliação, foto de pessoa ou contador de gente. Os dois usam `--glass`, `--shadow-float`, texto `#25231F` / `#55514A` (sobre ≈ fog-50: 13,9:1 e 7,0:1; cálculo manual, mistura aproximada por causa da transparência).

| | 375 | 1440 |
|---|---|---|
| A. Peça em destaque (Jarra Névoa, R$ 168) | linha de 313 × 92; raio 20; padding 12; miniatura 56 × 70 (raio 12) + nome 14/600 + preço Fraunces 18 + botão redondo **+** 44 × 44 contornado. Sobrepõe 20 px da base da cena (`margin-top: -20px`); padding-top do texto sobe para 28 | 288 × ~168; raio 20; padding 16; miniatura 64 × 80 + nome + preço; botão contornado "Adicionar" 44 de altura, largura total. Canto superior direito da cena: `top 32; right 32` |
| B. Selo "Fornada nº 14 · 8 peças" | pílula 32 px no canto superior direito (`top 12; right 12`); texto 13/600; abaixo de 600 px mostra só "Fornada nº 14" para não colidir com o botão de pausa | 220 × 72; raio 20; padding 14 18; linha 1 Fraunces 20 "Fornada nº 14", linha 2 13 px "8 peças · Curitiba". `top 32; left calc(42% + 32px)` |

Observação: "8 peças" é a contagem do carrossel Névoa em `index.html`; o moodboard dizia 20, que é o total da loja. Conferir com o UX antes de publicar. Esses cartões **substituem** `.hero__note` (sem duplicar o texto "Fornada nº 14 · Curitiba").

A usa o mesmo `data-add` do cartão do carrossel (mesmo id, mesma sacola). Estados do botão: hover inverte para `#25231F` com texto `#F4F1EC` (como `.add`); foco 3 px `#25231F`, offset 3; confirmado vira argila. Entrada: `settle` de 900 ms uma vez, sem flutuação em loop; com `prefers-reduced-motion` e com a pausa, nada se move. Sem `backdrop-filter` (ou com transparência reduzida), usa o fundo sólido `#F8F5F0`.

### 4.3 Faixa de vantagens em painel (P4)

Logo abaixo do painel do hero, dentro do container, `margin-top: var(--panel-gap)`.

| | 375 | 1440 |
|---|---|---|
| Painel | 337,5 de largura; fundo `#EAE6DF`; sem borda; raio 24; padding 20 | 1216 de largura; mesmo fundo; raio 28; padding 32 40 |
| Grade | 2 colunas, gap 20 × 16; item em coluna: ícone acima do texto | 4 colunas (≈ 267 cada), gap 24; ícone à esquerda do texto |
| Ícone | círculo 40 `#F4F1EC`, traço argila 24 px (5,99:1 sobre `#EAE6DF`, cálculo manual) | círculo 48, traço 28 |
| Texto | 14/1,35; título `#25231F` 600, linha 2 `#55514A` (6,34:1 sobre `#EAE6DF`, manual) | idem |

Não clicável: sem hover e sem foco. Os 4 benefícios e o texto não mudam.

### 4.4 Cartão de categoria pastel (P5)

| | 375 | 1440 |
|---|---|---|
| Cartão | 126 de largura (rolagem horizontal, 2,6 visíveis, como hoje); raio 20; padding 10 10 14; fundo = pastel da §3 | 224 × ≈ 292 (5 colunas, gap 24); raio 20; padding 16 16 20 |
| Imagem | quadrado 106; raio 14; fundo transparente com chão `rgb(37 35 31 / .06)` a 72% | quadrado 192; raio 14 |
| Texto | nome 14/600, até 2 linhas; contagem 13 `#55514A` | idem; nome 15 |

Hover (≥ 1024, ponteiro fino): `translateY(-4px)`, `--shadow-lift`, imagem `scale(1.06)` (como hoje), 200 ms. Foco: 3 px `#25231F`, offset 3, seguindo o raio 20. Ativo: sem elevação. Reduced motion: sem deslocamento nem zoom, só a sombra. Celular: sem hover; toque filtra como hoje.

### 4.5 Cartão de produto

Continua **sem caixa** (UI-001). Muda só o raio e o selo.

| | 375 | 1440 |
|---|---|---|
| Imagem | 144,6 de largura (`--card-w`), proporção 4:5, raio 16 | 286 × 357, raio 20 |
| Selo "Novo" / "Esgotado" | pílula 999; fundo `#F4F1EC` (ou `#25231F`); 13/600 caixa-alta; posição `top 10; left 10` (era 4 px de raio e 11 px de texto) | `top 12; left 12` |
| Corpo | nome 14/600, medida 13, preço Fraunces 22, botão 44 de altura em pílula (sem mudança) | idem |

Estados: hover (≥ 1024) imagem `scale(1.045)` + `--shadow-lift`; botão inverte para tinta no hover e fica argila ao confirmar; foco 3 px `#25231F`; "Esgotado" mantém borda tracejada e `disabled`. Fundos por coleção (`--tint-*`) inalterados.

### 4.6 Faixa "O ateliê" com números (P7)

Vira painel escuro dentro do container: fundo `#25231F`, raio 28 (375) / 32 (1440), margem lateral `--panel-gap`, padding 32 24 (375) / 64 64 (1440). Grade atual 5fr/7fr no desktop, empilhada no celular.

| | 375 | 1440 |
|---|---|---|
| Número | Fraunces 300, `opsz` 144, 44 px, `#F4F1EC` (13,9:1) | 72 px (`clamp(2.75rem, 2rem + 3vw, 4.5rem)`) |
| Unidade | Figtree 600, 0,4em (≈ 18 px), `#BDB7AC` ao lado do número | ≈ 29 px |
| Legenda | 14 px `#BDB7AC` (7,86:1 sobre `#25231F`, manual), até 3 linhas | 14 px, 2 a 3 linhas |
| Divisor | borda superior `rgb(244 241 236 / .18)`, padding 20 0 | 3 colunas, gap 32; borda superior, padding 24 0 |

Números: **1.240 °C** · **14ª** fornada · **1** ceramista, todos já presentes na página. Mudança de copy: "Dia a dia" e "Peça única" saem do numeral; o conteúdo das legendas deve ser reencaixado pelo UX (o cuidado com micro-ondas já está na Ajuda). Não interativo.

### 4.7 FAQ em cartões (P8)

| | 375 | 1440 |
|---|---|---|
| Lista | largura 337,5; gap 12; sem a linha superior de hoje | 768 (coluna 8fr); gap 16 |
| Cartão (`details`) | fundo `#EAE6DF`; raio 20; padding 0 20 | padding 0 28 |
| `summary` | altura mínima 64; Figtree 600 16 | altura mínima 72; 17 |
| Ícone | círculo 36 `#F4F1EC` com **+** (gira 45° ao abrir) | idem |
| Resposta | padding 0 0 20; `#55514A`, até 62ch | padding 0 0 28 |

Hover: fundo `#D9D4CB` (10,63:1 com `#25231F`, manual). Aberto: fundo `#F4F1EC` + borda 1 `#55514A` (7,00:1 contra o canvas; manual). Foco do `summary`: 3 px `#25231F`, offset 2, raio 20. Reduced motion: sem rotação. Celular: toque em toda a linha (≥ 64 de altura).

### 4.8 Rodapé em painel com assinatura (P9)

| | 375 | 1440 |
|---|---|---|
| Painel | margem lateral e inferior `--panel-gap` (18,75); fundo `#25231F`; raio 28; padding 40 24 0 | margem 32; raio 32; padding 64 64 0 |
| Grade | 1 coluna, gap 32 | `2fr 1fr 1fr` (já existe) |
| Links | 36 px de altura, `#BDB7AC`; hover `#F4F1EC` sublinhado; foco 3 px `#F4F1EC`, offset 3 | idem |
| Aviso legal | 13 px `#BDB7AC`, borda superior `rgb(244 241 236 / .16)` | idem |
| Assinatura "Bruma" | Fraunces 300, `opsz` 144, ≈ 28vw (105 px), `letter-spacing -0.04em`, `line-height .8`, cor `rgb(244 241 236 / .10)`, `aria-hidden="true"`, encostada na base e cortada ≈ 8% pelo raio | ≈ 26vw (374 px) |

A largura da palavra (≈ 2,6 a 2,9 em) é estimativa, **não medida**: o Developer ajusta o `font-size` para caber sem cortar o "B" nem o "a" em 375 e 1440. A assinatura é decorativa: o contraste não se aplica e o logotipo real continua no bloco da marca. Não interativa.

## 5. Proibições conferidas

Sem depoimentos, avaliações, estrelas, contadores de usuários, fotos de pessoas, marquee ou cor nova de ação; formas diagonais e recortes orgânicos do moodboard ficam de fora. Nenhuma imagem de terceiros entra no site. Nenhum texto passa de uma cor decorativa para a de ação.

## 6. Riscos e pendências

1. **Itálico em argila** (§2) contradiz UI-001 §5.2; exige decisão do proprietário. Plano B definido.
2. **Contrastes são manuais**, sem conferência por script; pedir a Quality para refazê-los (inclui os três pares de hero em vidro, que dependem do fundo atrás).
3. **Sem render.** Cartões flutuantes sobre a cena (A no celular, B no desktop) podem cobrir peças ou colidir com o botão de pausa; precisa de captura em 375 e 1440.
4. **Copy**: "8 peças" no selo e os numerais da faixa "O ateliê" dependem de aprovação do UX.
5. Texto de 11 px (selos, contador da sacola) existente já viola a regra de ≥ 13 px de UI-001; esta revisão sobe os selos para 13 px, o contador não foi tratado.
6. Dois painéis escuros (ateliê, rodapé) somados ao hero claro: avaliar o ritmo visual no render.
7. Figma não usado; nenhum frame ID existe. Arquivos alterados fora deste documento: nenhum.

## 7. Implementação (sessão do projeto, 2026-10-22)

Aplicado em `site/styles.css` e `scripts/gerar_site.py` (regera `site/index.html`). Decisões tomadas na implementação:

- Itálico em argila `#8A3F22`, como o moodboard pede (recomendação do agente); no painel escuro, argila clara `#EFD9CC`. Plano B continua disponível se o proprietário preferir.
- Selo do hero usa a contagem real do catálogo (8 peças da Névoa), calculada pelo gerador.
- Legendas da faixa "O ateliê" reencaixadas: micro-ondas/lava-louças foi para 1.240 °C, a variação de tom para 14ª fornada, e "1 ceramista" ganhou "torneada e esmaltada à mão pela mesma pessoa".
- Contrastes refeitos por script: `evidence/UI-003/contrast-check.json` (todos ≥ 4,5:1, iguais ao cálculo manual).
- Capturas e testes de interação: `evidence/UI-003/render/`.

## 8. Refino de margens no celular (pedido do proprietário, 2026-10-22)

O proprietário viu respiro desigual entre a esquerda e a direita no celular. Medição por script (`evidence/UI-003/a11y/margens-medidas.txt`, 320 a 414 px) achou três causas:

1. `scrollbar-gutter: stable` reservava 15 px à direita mesmo no celular, então tudo ficava deslocado para a esquerda. Agora vale só em telas ≥ 1024 px com mouse.
2. A pílula "Coleção Névoa · Primavera 2026" não quebrava linha e alargava a coluna do hero além do painel, encurtando o respiro direito do texto (24 px à esquerda, 9 px à direita). A grade do hero agora é `minmax(0, 1fr)`, e abaixo de 420 px a pílula mostra só "Coleção Névoa".
3. Os recuos internos variavam (12, 20 e 24 px). Agora a regra é uma só: 24 px dentro de todo painel e cartão grande (hero, cartão flutuante, vantagens, ateliê, FAQ, rodapé). Os botões dos cantos do hero ("Pausar animação" e o selo da fornada) ficam a 16 px das duas bordas, espelhados.

Resultado: borda esquerda = borda direita em todos os blocos, em todas as larguras medidas. A exceção é proposital: o trilho dos carrosséis e das categorias corta o próximo cartão na direita (regra do proprietário). Acessibilidade: axe-core 4.10.2 em 320, 375, 768 e 1440 px, 0 violações (`evidence/UI-003/a11y/axe.json`). As duas que apareceram foram corrigidas: o aviso do topo virou região nomeada e a assinatura "Bruma" virou pseudo-elemento decorativo.
