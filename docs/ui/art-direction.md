# Direção de arte: Ateliê Bruma (UI-001)

**Projeto:** piloto-01 · **Task:** UI-001 · **Agente:** eixo-ui-art-director · **Data:** 2026-10-22
**DNA:** v0.2.0 (aprovado somente como briefing fictício) · **Depende de:** UX-001 (aprovado pelo proprietário em 2026-10-22)
**Status deste documento:** PROPOSTA, **NÃO APROVADA**. Marca, logotipo e direção são **FICTÍCIOS** e aguardam aprovação humana antes do Developer.

> Legenda: **FATO** (fonte externa citada na pesquisa) · **HIPÓTESE** (inferência a validar) · **FICTÍCIO** (inventado para o piloto) · **DECISÃO** (escolha desta UI, sujeita a aprovação). "Pesquisa §x" = `docs/ux/research/pesquisa-mercado.md`.

## 0. O que foi e o que não foi feito (leia primeiro)

| Item | Situação |
|---|---|
| Figma | **NÃO REALIZADO.** O Figma MCP não está conectado neste runtime. Não existe arquivo, frame ou ID de frame. Entrega por arquivos em `docs/ui/`. |
| Render / inspeção visual | **Por este agente: NÃO REALIZADO.** Este agente não abriu nenhum SVG ou HTML em navegador. **Pela revisão independente: a prancha `preview.html` foi renderizada** (Playwright + Chromium headless, `evidence/UI-001/render-check.json`), o que mediu o header a 320 px, o carregamento dos 5 SVGs e achou rolagem horizontal (corrigida na rodada 3 por análise de CSS, **sem nova medição**). Esse registro é de medidas, não de avaliação visual: ninguém avaliou como a prancha ou o símbolo *parecem*. |
| Execução de scripts | **Por este agente: NÃO REALIZADA.** Os contrastes foram **calculados à mão** (fórmula WCAG 2.x) por este agente e **conferidos por script pela revisão independente** (`evidence/UI-001/contrast-check.json`: 20 pares, diferença máxima 0,04). A borda do placeholder passou a ink-700 na rodada 3 (resolve C16b, 4,43 medido). |
| Verificação de licença das fontes | **NÃO REALIZADA online.** As licenças (SIL OFL 1.1) são citadas com os repositórios de origem, a partir do conhecimento prévio do agente. O Developer deve baixar os arquivos `OFL.txt` das fontes e arquivá-los. |
| Pesquisa de anterioridade do logotipo | Não feita (marca fictícia). |
| Teste com pessoas | Não houve. Nada aqui é resultado de usabilidade. |

## 1. Leitura de marca

| Dimensão | Leitura | Tipo |
|---|---|---|
| Quem é | Ateliê de uma ceramista; cerâmica utilitária autoral em grés de alta temperatura, para a mesa do dia a dia. | FICTÍCIO (Pesquisa §3.1) |
| Nome | "Bruma" = névoa. Esmalte fosco, tons neutros, bordas que se diluem; a variação de fornada é parte da peça. | FICTÍCIO (conceito verbal, Pesquisa §3.1; `content-structure.md` §3) |
| Promessa | "Uma fornada por mês, para usar todo dia sem medo." | FICTÍCIO |
| Público | Mulheres de 25 a 44 anos, classes B/C, ensino superior; compram para presentear (53%) ou decorar (47%). | FATO (Sebrae/RJ, Pesquisa §1.1) aplicado ao cliente fictício; adequação à marca = HIPÓTESE |
| Contexto de uso | Celular, vindo de rede social (60% descobrem novidades ali); decisão 55% emocional. | FATO + HIPÓTESE (Pesquisa §2.1) |
| Barreiras | Acabamento/qualidade (39%) e preço alto (27%). | FATO (Pesquisa §1.1) |
| Tom | Calmo, direto, caloroso, sem urgência, sem escassez, sem prova social inventada. | DECISÃO (UX: `content-structure.md` regras gerais) |
| O que a identidade visual precisa fazer | (1) Transmitir cuidado e acabamento sem foto (só há placeholders). (2) Deixar o caráter fictício **visível e honesto** sem que a página pareça "quebrada". (3) Dar ao CTA um único peso dominante. (4) Funcionar em celular, 32 px de logotipo no header, 320 px de largura. | Objetivos de UX (`handoff-ui.md` §2) |
| Estilo a evitar | Aspecto de template de loja; "rústico" com madeira e linho clichê; estrelas, selos, medalhas; gradientes que prejudiquem leitura; a identidade da EIXO. | Restrição (`handoff-ui.md` §3) |

**Consequência principal de projeto (DECISÃO):** como todas as imagens são placeholders, a página não pode depender de fotografia para ter qualidade percebida. A qualidade tem de vir de **tipografia, proporção, ritmo e cor**. Por isso o placeholder é tratado como elemento de design (§5.7), não como "caixa cinza".

## 2. Curadoria: o que foi realmente inspecionado

**Inspecionado (lido integralmente):** `docs/ux/handoff-ui.md`, `docs/ux/ux-spec.md`, `docs/ux/content-structure.md`, `docs/ux/acceptance-criteria.md`, `docs/ux/research/pesquisa-mercado.md`, `docs/project-dna.md`, `CLAUDE.md`.

**NÃO inspecionado:** os sites de referência citados na pesquisa (Ateliê Ise, AMME Cerâmica, Cafaz Ateliê, Ana Rojo), Dribbble, Behance e qualquer vídeo. Não houve navegação web nem captura de tela. Do que se sabe deles, só consta o que a Pesquisa §1.3 descreve em texto (navegação por uso, séries nomeadas, explicação de material e cuidados, "beleza na imperfeição"). **Nenhum layout, cor ou tipografia desses sites foi observado**, portanto nenhum foi imitado nem pode ser "citado como referência visual".

**Princípios extraídos da pesquisa textual (HIPÓTESE, não observação de frames):**
1. A prova de qualidade vem de **material, processo e origem**, não de elogios (Pesquisa §1.3, §2.2). Traduz-se visualmente em tipografia editorial e texto bem composto, e não em selos.
2. **Imperfeição como valor** (Ana Rojo, Pesquisa §1.3): a identidade não pode ser rígida e fria; as bordas e o traço do logotipo são arredondados e as formas do site têm "bordas que se diluem" (arco, raios generosos).
3. **Preço e medida à vista** (Pesquisa §2.3): precisam de hierarquia tipográfica clara, não de botões.
4. **Presente como caso de uso nº 1** (Pesquisa §3.2): a coleção deve poder ser lida rapidamente por peças, em coluna única no celular.

**Repertório geral** (conhecimento do agente, não consulta nesta sessão): mercado de cerâmica autoral tende a bege/terracota, serifas suaves, muito espaço e fotografia de luz natural. Isso é justamente o risco de lugar-comum que a direção escolhida tenta contornar (§3 e §7).

## 3. Duas direções distintas

### Direção A: "Névoa quieta" (ESCOLHIDA)

| Eixo | Decisão |
|---|---|
| Mood | Manhã de névoa na cozinha. Calmo, editorial, atento ao detalhe. Baixo contraste de superfícies, alto contraste de texto. |
| Cor | Neutros quentes de névoa (`#F4F1EC`, `#EAE6DF`, `#D9D4CB`), tinta quase preta quente (`#25231F`), **uma única cor de ação**: argila escura (`#8A3F22`). Azul-névoa (`#B9C4C8`) só em gradientes decorativos. |
| Tipografia | **Fraunces** (serifa de contraste suave, eixos "soft"), peso 300 a 400, para títulos e preços; **Figtree** (sans geométrica humanista) para texto e navegação. |
| Composição | Coluna única no celular, com texto antes da imagem; assimetria controlada no desktop (texto à esquerda, arco de imagem à direita; manifesto em 2 colunas); faixas alternando canvas e surface; **cartões sem caixa** (hairline, imagem, texto). Muito espaço vertical (64 px no celular, 112 px no desktop). |
| Imagem | Placeholders em **arco** (hero) e retângulos 4:5 de raio generoso (peças); fotografia futura: luz natural difusa, fundo de névoa, esmalte fosco, pouca saturação. |
| Logotipo | Vaso garrafa em contorno + duas faixas de bruma + nome em duas linhas, traço monolinear. |
| Motivo gráfico | **Traço tracejado = ilustrativo/fictício** (placeholders, etiquetas "exemplo"). Faz a honestidade do projeto parte da identidade em vez de um aviso colado. |
| Risco | Parecer "mais um site bege de cerâmica"; mitigado pelo traço tracejado, pelo logotipo próprio e pelo uso restrito da argila apenas para ação. |

### Direção B: "Esmalte" (não escolhida)

| Eixo | Decisão |
|---|---|
| Mood | Oficina, vidrado, cor saturada. Gráfico, contrastado, mais "marca de design" do que "ateliê". |
| Cor | Osso `#EFEAE0`, cobalto `#1F3A5F`, âmbar `#C58B2B`, celadon `#7FA79A`, coral `#D8664A`, carvão `#1A1A1A`. Blocos de cor chapados como amostras de esmalte. |
| Tipografia | Grotesca de alto contraste e peso (família tipo "Bricolage Grotesque", OFL; **não verificada** nesta sessão), títulos enormes, texto em sans neutra. |
| Composição | Blocos retangulares justapostos, bordas retas, grade modular visível, numerais grandes. |
| Imagem | Placeholders como amostras de cor lisa. |
| Logotipo | Monograma "B" de bojos sobrepostos em cobalto. |
| Risco | Competir com fotografia futura; parecer agressivo para um público de presente/decoração; exigir validação de contraste em várias combinações cromáticas. |

### Escolha justificada

**Escolha: A.** Razões:
1. **Adequação ao público e ao tom (HIPÓTESE):** o público é predominantemente feminino, 25 a 44 anos, decisão 55% emocional (Pesquisa §1.1). A promessa é calma ("uma fornada por vez"). B comunica energia e ruído, em desacordo com a promessa.
2. **Fidelidade ao nome:** "bruma" pede tons suaves e bordas que se diluem (`content-structure.md` §3). A cumpre isso; B o contradiz.
3. **Placeholders:** com todas as imagens sendo placeholders, B (blocos chapados saturados) teria muito mais peso visual de "vazio colorido" do que A, cujo placeholder em névoa tracejada se lê como "espaço reservado" sem gritar.
4. **Acessibilidade:** A usa uma só cor de ação e um par texto/fundo dominante de alto contraste; B multiplicaria pares de cor a validar.
5. **Custo:** A é mais simples de implementar (poucos tokens, sem ilustração).

A recusa de B é uma **decisão de projeto**, não prova de que A seja "melhor visualmente". Nenhuma das duas foi testada com pessoas.

## 4. Logotipo (resumo; detalhes em `logo/README.md`)

Vaso garrafa de cerâmica em contorno (peça nº 6 da coleção; **desenho revisado na rodada 2** para ter lábio, gargalo curto, ombro marcado e base plana, e não parecer frasco de laboratório; decisão em `logo/README.md` §7) com duas faixas de bruma de comprimentos diferentes; nome "Ateliê / Bruma" em duas linhas, letras monolineares desenhadas como paths. Lockup 81 × 32 px. Versões: principal (tinta + argila), monocromática para fundo claro, monocromática para fundo escuro, ícone (claro e escuro). Os 7 requisitos funcionais do handoff estão verificados caso a caso no README, com a distinção **PROJETO** (atendido por especificação) e **A CONFIRMAR** (precisa de render real). **FICTÍCIO, NÃO APROVADO.**

## 5. Sistema visual

Fonte executável: `tokens.json` e `tokens.css` (mantidos à mão em sincronia; nenhum gerador executado).

### 5.1 Cor: primitives

| Token | Hex | Papel |
|---|---|---|
| fog-50 | `#F4F1EC` | canvas |
| fog-100 | `#EAE6DF` | superfície, hover |
| fog-200 | `#D9D4CB` | etiqueta, estado ativo, divisor decorativo |
| stone-300 | `#BDB7AC` | texto secundário em fundo escuro |
| ink-700 | `#55514A` | texto secundário; linha forte (borda de placeholder; rodada 3 retirou o primitive stone-500) |
| ink-900 | `#25231F` | texto principal, foco, rodapé |
| clay-700 | `#8A3F22` | ação primária, links |
| clay-800 | `#6F3019` | hover da ação |
| clay-900 | `#5A2813` | ativo da ação |
| mist-300 | `#B9C4C8` | **decorativo apenas** (nunca texto, nunca componente) |

### 5.2 Cor: aliases semânticos
`background/canvas` fog-50 · `background/surface` fog-100 · `background/chip` fog-200 · `background/inverse` ink-900 · `text/primary` ink-900 · `text/secondary` ink-700 · `text/link` clay-700 · `text/inverse` fog-50 · `text/inverse-secondary` stone-300 · `action/primary` clay-700 · `action/primary-hover` clay-800 · `action/primary-active` clay-900 · `action/on-primary` fog-50 · `border/default` fog-200 (decorativo) · `border/strong` ink-700 · `focus/ring` ink-900 · `focus/ring-inverse` fog-50.

**Regras de uso (DECISÃO):**
- Argila (clay) **só** para ação (CTA, links, estado do logotipo). Nada decorativo em argila, para o único CTA conservar peso.
- Texto **nunca** sobre gradiente de névoa: sobre o placeholder, texto só em caixa sólida (legenda).
- Informação **não depende só de cor**: links sublinhados; etiquetas com texto e traço tracejado; hover do header com sublinhado.
- `border/default` é decorativo e **não pode** ser a única marca de um controle ou limite informativo.
- Todos os pares texto/fundo e componente/fundo estão na tabela de `ui-handoff.md` §7, calculados à mão e **conferidos por script pela revisão independente** (`evidence/UI-001/contrast-check.json`).

### 5.3 Tipografia e licenças

| Papel | Família | Pesos | Licença | Origem |
|---|---|---|---|---|
| Títulos, preços | **Fraunces** (variável; eixos opsz, wght, SOFT, WONK) | 300, 400 | SIL Open Font License 1.1 | Undercase Type, <https://github.com/undercasetype/Fraunces> (arquivo `OFL.txt` do repositório; também distribuída em <https://github.com/google/fonts/tree/main/ofl/fraunces>) |
| Texto, navegação, UI | **Figtree** (variável) | 400, 500, 600 | SIL Open Font License 1.1 | Erik D. Kennedy, <https://github.com/erikdkennedy/figtree> (também <https://github.com/google/fonts/tree/main/ofl/figtree>) |
| Texto da licença | OFL 1.1 | | | <https://openfontlicense.org/> |

- **Não verificado nesta sessão:** os URLs acima e o conteúdo de cada `OFL.txt` não foram baixados nem conferidos (sem acesso de rede autorizado). O Developer deve baixar as fontes e o `OFL.txt` de cada repositório, **arquivar a licença no projeto** e, só então, tratar o uso como licenciado. Se a verificação falhar para alguma, usar a pilha de fallback (fontes do sistema) até haver substituta.
- **Auto-hospedar** em WOFF2 (sem requisição a serviço de terceiros; evita envio de IP do visitante e dependência externa, e respeita "sem recursos externos" do escopo). Subconjunto latino com acentos de português.
- Pilhas de fallback: display `"Fraunces", "Iowan Old Style", "Palatino Linotype", Georgia, serif`; texto `"Figtree", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`. As fontes de fallback são do sistema do usuário; nada é distribuído.
- `font-display: swap` com `size-adjust`/métricas de fallback ajustadas pelo Developer para limitar CLS.
- O wordmark do logotipo **não** usa fonte (paths próprios).

### 5.4 Escala tipográfica

| Nível | Tamanho | Entrelinha | Peso | Uso |
|---|---|---|---|---|
| h1 | `clamp(2.25rem, 1.4rem + 3.2vw, 4rem)` (36 px a 320/375; ~47 px a 768; ~55 px a 1024; 64 px de ~1300 px em diante) | 1,1 | Fraunces 300, tracking −0,01em | hero |
| h2 | `clamp(1.75rem, 1.4rem + 1.8vw, 2.5rem)` | 1,2 | Fraunces 400 | seções |
| h3 | 1.375rem (22 px) | 1,2 | Fraunces 400 | peças, blocos |
| subtítulo | `clamp(1.1875rem, 1.1rem + .5vw, 1.375rem)` | 1,5 | Figtree 400 | hero |
| corpo | 1.0625rem (17 px) | 1,6 | Figtree 400 | texto, medida até 62ch |
| nav | .8125rem (<360 px), .875rem (360 a 767), 1rem (≥768) | 1,4 | Figtree 500/600 | header |
| etiqueta/legenda | .8125 a .875rem | 1,4 | Figtree 600/400 | "exemplo", placeholder |

Nenhum texto abaixo de 13 px. Texto em `rem`: respeita o tamanho preferido do usuário e o zoom de 200%.

### 5.5 Espaçamento, grade, raio

- **Espaçamento:** base 4 px (4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128). Seções: 64 px de respiro vertical no celular, 112 px a partir de 1024 px.
- **Grade:** coluna única até 767 px; contêiner de 72rem (1152 px) centralizado; gutter `clamp(1rem, 5vw, 2rem)`. Coleção: 1 / 2 / 3 colunas (≤767 / 768 a 1023 / ≥1024), gap 32 a 40 px. Detalhes por seção em `ui-handoff.md` §6.
- **Raio:** 4 (etiquetas, retangulares de propósito para não parecerem selos) · 10 (hover do logo, skip link) · 20 (placeholders das peças) · arco `999px 999px 10px 10px` (hero) · pílula 999 (**só** o CTA).
- **Elevação:** sem sombras. Hierarquia por tom, espaço e linha.

### 5.6 Foco
Contorno sólido de 3 px, `ink-900` (fundo claro) ou `fog-50` (fundo escuro), offset 3 px (2 px em links de texto e no logotipo). Razão 13,92:1 contra canvas e 12,61:1 contra surface (cálculo manual). Funciona em todos os fundos da página; o offset deixa uma folga de fundo entre o anel e o CTA (argila), então o anel é comparado ao fundo, não ao botão.

### 5.7 Tratamento dos placeholders (peça central da direção)

- **Forma:** caixa de proporção fixa (`aspect-ratio`, 4:5 nas peças e no hero; evita CLS). Hero em **arco** (`border-radius: 999px 999px 10px 10px`); peças em retângulo de raio 20.
- **Preenchimento:** névoa decorativa: dois gradientes radiais de `mist-300` translúcido sobre um degradê vertical `fog-100` → `fog-200`. É decoração; nenhum texto repousa diretamente sobre ele.
- **Borda:** 2 px **tracejada** em `ink-700` (`border/strong`). O tracejado é o idioma visual de "ilustrativo/fictício" em todo o projeto. Histórico: a rodada 2 usava `stone-500`, que caía a 2,56:1 contra o pior caso do degradê (`mist-300` puro; C16b, falha confirmada pelo script da revisão). A rodada 3 adotou `ink-700` por padrão razoável (4,43:1 no pior caso, medido pela revisão), reversível pelo proprietário; detalhes em `ui-handoff.md` §5.6 e §7. Efeito de design: a borda fica mais escura e mais presente; ninguém avaliou visualmente se o placeholder continua "quieto".
- **Legenda obrigatória** "Imagem ilustrativa (placeholder)": caixa sólida `fog-50`, texto `ink-700` 14 px (7,00:1), no canto inferior esquerdo, **dentro** da área do placeholder, em `<figcaption>`. Não pode ser ocultada, nem por CSS responsivo.
- **Descrição:** `role="img"` + `aria-label` com o alt de `content-structure.md` (no `<div>` placeholder), ou `<img alt>` quando houver arquivo real.
- **Imagem falhou:** o contêiner mantém proporção, gradiente e borda; o `alt` aparece como texto `ink-700` 14 px **em caixa sólida `fog-50`** no canto superior esquerdo (mesma regra da legenda: texto nunca direto sobre o gradiente); legenda permanece no canto inferior esquerdo. (Corrigido na rodada 2: a prancha da rodada 1 pousava o alt direto sobre o gradiente, contra a regra de §5.2.)
- **Fotografia futura (orientação, não asset):** luz natural difusa, fundo liso de tom névoa, esmalte fosco, enquadramento 4:5 que sobreviva ao corte em arco no hero; fotos devem ser do próprio ateliê ou licenciadas por escrito antes de entrar. `assets_approved` continua `false`.
- **Ícones:** nenhum pacote de ícones. Qualquer glifo (ex.: seta) deve ser CSS/SVG próprio e documentado. Nesta proposta não há nenhum.

### 5.8 Movimento
- Só transição de cor de fundo/texto em 120 a 200 ms em hover/ativo. Nada se move sozinho; nenhum carrossel, parallax ou animação de entrada; **nenhuma animação ambiente de "névoa"**: seria o recurso mais óbvio e vai contra "sem animações que atrasem leitura".
- Rolagem suave **apenas** com `prefers-reduced-motion: no-preference` (CSS: `scroll-behavior`). Com `reduce`: `scroll-behavior: auto` e durações 0 s (já em `tokens.css`).
- Foco aparece de imediato, sem transição.

## 6. Composição orientada ao conteúdo

Resumo; especificação por seção e breakpoint em `ui-handoff.md` §6.

| Seção | Idéia de composição |
|---|---|
| Header | Fixo, 56 px. Logotipo à esquerda (32 px de altura), três links de texto à direita, sem fundo e sem competir com o CTA. |
| Hero | Texto primeiro: etiqueta fictícia, h1 leve em Fraunces 300, subtítulo, apoio, **CTA único em argila**. Imagem em arco depois (celular) ou ao lado (≥768 px). |
| Manifesto | Faixa `surface`. Desktop: título e introdução à esquerda, três afirmações à direita com hairline. Sem ícones, sem numerais decorativos. |
| Coleção | Canvas. Cartões sem caixa: hairline em tinta, imagem, nome, medida, preço em Fraunces. "Ideia de presente" como faixa de texto com régua lateral em argila. |
| Material | Faixa `surface`. Quatro blocos em 2 × 2 no desktop, empilhados no celular. |
| Contato | Lista de descrição com hairlines, e-mail em destaque sublinhado, etiqueta "dados de exemplo". |
| Rodapé | Fundo `ink-900`; logotipo monocromático claro, aviso de marca fictícia, "Voltar ao início". |

## 7. Crítica visual independente (autocrítica; não substitui revisão por outro agente ou pessoa)

Atenção: esta crítica é feita pelo próprio autor, que **não renderizou nada**, e portanto **não é independente**. A revisão independente renderizou a prancha só para medir (rolagem, header a 320 px, SVGs; `evidence/UI-001/render-check.json`), não para avaliar visualmente. Ela lista o que um revisor deve procurar. Quality/QA devem repetir com a página renderizada e olhada.

| Risco | Observação | Mitigação proposta |
|---|---|---|
| Aspecto de template | Paleta bege + serifa + muito espaço é o clichê do setor. | Tracejado como motivo, logotipo próprio, argila só na ação, cartões sem caixa. Revisor deve julgar se bastou. |
| Excesso de cartões | Seis peças repetidas em grade. | Cartões sem caixa/sombra; apenas hairline superior. |
| Página "rala" | UX já aponta o risco (`ux-spec.md` §7, heurística 8). Com placeholders, a página pode parecer vazia. | Escala tipográfica com contraste, faixas alternadas, arco do hero. Pode não bastar; só teste com pessoas e fotos reais dirão. |
| Peso visual dos placeholders | Seis blocos de névoa tracejada podem dominar a coleção. | Gradiente suave, legenda pequena; avaliar redução de altura (3:4) após render. |
| Títulos viúvos/quebras | h1 em 2 a 3 linhas a 320 px. | `text-wrap: balance` em h1/h2/h3 (melhoria progressiva); verificar em 320 e 375. |
| Logotipo a 32 px | Traço de 1,5 px pode ficar frágil em telas 1x. | Fallback de traço 1,75 (README do logotipo, §4.1). Item de maior incerteza. |
| Símbolo lido como frasco de laboratório | Apontado pelo revisor na rodada 2; aceito e redesenhado (lábio, gargalo curto, ombro, base plana). Faixas de bruma ainda podem lembrar graduação. | `logo/README.md` §7. Reavaliar com render; teste de reconhecimento com pessoas não feito. |
| Header estreito (320 px) | A revisão mediu a maquete de 320 px em uma linha (conteúdo termina em 308 px de 320), **com fonte de fallback** porque Figtree não está embutida; com a fonte real a largura pode mudar. Estimativa anterior: folga de ~5 px contando a área de toque do logotipo (89 px) e o espaço de 8 px. | Fonte 13 px e `padding-inline` de 4 px nos links abaixo de 360 px (ganha ~12 px), e `flex-wrap`. Medir (`ui-handoff.md` §6.1). |
| Fontes | Fraunces tem personalidade ("wonk"); em pesos baixos pode perder contraste em telas ruins. | Peso 300 só em ≥28 px; h3 e preços em 400; ajustar `opsz`. Avaliar após render. |
| Contraste | Calculados à mão e conferidos por script pela revisão (20 pares, diferença máxima 0,04). C16b (stone-500 sobre mist-300, 2,56) falhava; borda trocada para ink-700 (4,43). | Contraste de cor não é conformidade WCAG; leitor de tela e teclado seguem não testados. |
| Rolagem horizontal da prancha | A revisão mediu rolagem horizontal em 320 a 1024 px (causa: item de grid com `min-width:auto` envolvendo a maquete de 1024 px). | Corrigida na rodada 3 por análise de CSS (`minmax(0,1fr)` e `min-width:0`); **pede nova medição**. |
| Logo e título em fontes de natureza diferentes | Wordmark monolinear geométrico vs. títulos serifados. | Intencional (marca vs. editorial). Revisor pode discordar. |
| Tracejado como "erro" | Pode ser lido como componente quebrado. | Legenda e etiqueta explícitas; mantém honestidade exigida pelo handoff. |

## 8. Autoavaliação pela rubrica (ferramenta de crítica, não medida objetiva)

Notas do próprio autor, sem avaliação visual (a renderização da revisão mediu, não julgou) e sem teste com pessoas. Não foram reavaliadas na rodada 3. Servem para priorizar a revisão, não como aprovação.

| Dimensão | Peso | Nota (autor) | Nota ponderada | Comentário |
|---|---:|---:|---:|---|
| Fidelidade à marca e originalidade | 25 | 19 | 19 | Conceito coeso (vaso + bruma + tracejado); original no logotipo; risco de clichê no restante. |
| Composição, tipografia e hierarquia | 20 | 14 | 14 | Hierarquia bem definida no papel; sem avaliação visual não há como julgar ritmo real. |
| Imagens, produto e conteúdo | 20 | 9 | 9 | Só placeholders. Tratamento digno, mas sem produto visível. Limite estrutural do piloto. |
| Clareza de UX e conversão | 15 | 12 | 12 | CTA único, header sem hambúrguer, preço visível; respeita UX. |
| Consistência e acabamento | 10 | 7 | 7 | Tokens coerentes; os SVGs carregam (medido pela revisão), mas ninguém os avaliou visualmente, o que pesa contra acabamento. |
| Responsividade e acessibilidade visual | 10 | 7 | 7 | Contrastes conferidos por script pela revisão; alvos projetados; rolagem da prancha corrigida sem nova medição. |
| **Total** | **100** | | **68** | Falhas críticas de marca, legibilidade ou acessibilidade bloqueiam entrega independentemente da nota; **nenhuma foi identificada, mas ninguém avaliou o resultado visualmente** (ver §0). |

## 9. Conferência com as restrições do handoff

| Restrição | Situação |
|---|---|
| Ids e ordem das seções, `#colecao` | Respeitados (ver `ui-handoff.md` §6). |
| CTA único, sem segundo botão primário | Sim; links do header são texto simples. |
| Header sempre visível, sem hambúrguer | Sim; fixo, com `scroll-padding-top`. |
| Cartão com nome, medida e preço visíveis; sem comprar/carrinho/ver mais/favoritar/filtros/carrossel | Sim. |
| Contato é texto, sem formulário | Sim. |
| Etiquetas "exemplo" e legenda "Imagem ilustrativa (placeholder)" visíveis e não ocultáveis | Sim. |
| Sem depoimentos, estrelas, selos, "mais vendido" | Sim; etiquetas são retangulares e tracejadas, não selos. |
| Sem identidade EIXO | Sim; paleta, nome, tipografia e símbolos próprios. |
| Sem assets sem licença | Sem imagens, sem ícones de terceiros; fontes OFL com licença a arquivar. |
| Movimento respeita `prefers-reduced-motion` | Sim. |
| Logotipo: 7 requisitos | `logo/README.md` §4. |
| Nada marcado como aprovado | Correto. |
