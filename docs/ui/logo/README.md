# Logotipo do Ateliê Bruma (UI-001)

**Status: FICTÍCIO, NÃO APROVADO.** Proposta de logotipo para a marca fictícia Ateliê Bruma, por decisão do proprietário em 2026-10-22 ("A logo precisa propor um logotipo"). Depende de aprovação humana posterior. Não é identidade de cliente real.

**O que NÃO foi feito, e por quem:** o agente que desenhou o logotipo **não renderizou nem abriu** nenhum arquivo em navegador/visualizador; a geometria foi desenhada e conferida por cálculo de coordenadas. A **revisão independente** carregou os 5 SVGs com Playwright + Chromium headless (`evidence/UI-001/render-check.json` e `logo-32px-check.json`): todos válidos e renderizados em 81 × 32 (lockups) e 32 × 32 (ícones), e usados na prancha. Isso confirma que **os arquivos carregam e têm o tamanho nominal**; **ninguém avaliou visualmente o símbolo** (leitura como vaso, traço de 1,5 a 32 px, encaixe das letras), pois esses registros não contêm julgamento visual. Toda afirmação de legibilidade abaixo segue sendo **projeção de projeto**, a confirmar por QA/Quality olhando o render.

## 1. Arquivos

| Arquivo | Uso | Cores |
|---|---|---|
| `logo-principal.svg` | Header e contextos de fundo claro | tinta `#25231F` + argila `#8A3F22` nas duas faixas de bruma |
| `logo-mono-fundo-claro.svg` | Fundo claro quando só uma cor é possível (impressão P&B, carimbo, relevo) | `#25231F` |
| `logo-mono-fundo-escuro.svg` | Rodapé escuro e qualquer fundo `#25231F` | `#F4F1EC` |
| `icone.svg` | Forma reduzida: favicon, avatar. Vaso cheio com faixas vazadas | `#25231F` |
| `icone-fundo-escuro.svg` | Idem em fundo escuro | `#F4F1EC` |

Dimensões nominais: lockup `81 × 32` (viewBox `0 0 81 32`; 1 unidade = 1 px na altura de 32 px). Ícone `32 × 32`. Fundo transparente. Não há `<text>`, `<image>`, fonte, script, filtro ou referência externa nos arquivos; só `<path>` e um `<circle>` (ponto do "i").

## 2. Conceito e justificativa

- **Símbolo:** um **vaso garrafa de cerâmica** (a peça nº 6 da coleção Névoa, `content-structure.md` §4), em contorno, com **lábio** (borda levemente aberta), **gargalo curto**, **ombro marcado** (curva em S) e **base plana**, atravessado por **duas faixas de bruma** horizontais de comprimentos diferentes, como névoa baixa que não cobre o objeto inteiro. (Desenho revisado na rodada 2; ver §7.) Une as duas ideias do nome: objeto de cerâmica (o ofício) e névoa (o nome). É silhueta de produto, não selo, medalha, estrela ou símbolo de certificação.
- **Nome:** "Ateliê / Bruma" em **duas linhas**, letras minúsculas de traço monolinear com terminais arredondados, construídas só com linhas, arcos de círculo e cantos arredondados (bacia/tigela = semicírculo; "a" e "e" = círculo). O traço do contorno do vaso tem a mesma espessura (1,5) do traço das letras, então símbolo e nome parecem desenhados com a mesma ferramenta (um pincel/arame fino), em contraste com os títulos serifados do site (que dão o lado "ateliê/editorial").
- **Por duas linhas:** a 32 px de altura, uma linha única "Ateliê Bruma" ao lado do símbolo teria cerca de 170 px de largura e tiraria o espaço dos três links do header a 320 e 375 px. Em duas linhas o lockup tem 81 px de largura com altura de x de ~8,5 px (traço incluso), o que deixa o nome legível sem quebrar a navegação.
- **Por que não uma forma "bruma" genérica (gradiente, esfumado):** gradientes e transparências não sobrevivem à versão monocromática nem ao tamanho de 32 px. A "bruma" aqui é feita de **interrupções de linha**, que funcionam em uma cor só.
- **Cuidado de originalidade:** a construção foi desenhada nesta tarefa; nenhuma fonte, ícone ou logotipo de terceiros foi usado como base ou traçado. Não foi feita busca de anterioridade/marca registrada (a marca é fictícia; em marca real isso seria obrigatório).

## 3. Construção (para reprodução e revisão)

- Grade: 1 unidade = 1 px a 32 px de altura. Traço 1,5, `stroke-linecap: round`, `stroke-linejoin: round`.
- Linha 1 "Ateliê": linha de base y = 14,8; altura de x (linha de centro) 7,0 (y 7,8 a 14,8); ascendente do "l" até y = 2,6; "A" maiúsculo com altura 12 (y 2,8 a 14,8); acento circunflexo do "ê" com vértice em y = 2,6.
- Linha 2 "Bruma": linha de base y = 30,8; altura de x idêntica (7,0); "B" com altura 12 (y 18,8 a 30,8). Distância livre entre as duas linhas (do fundo do traço da linha 1 ao topo do "B"): ~2,5.
- Símbolo (revisado): eixo de simetria em x = 10. Lábio: barra de x 6,6 a 13,4 em y = 2, com 1,6 de altura, estreitando em diagonal até o gargalo (x 8 a 12, largura 4; y 4,6 a 8,2). Ombro: curva cúbica em S de (12; 8,2) a (19; 17), ponto médio em ~(15,5; 11,2). Corpo: largura máxima 18 (x 1 a 19, em y = 17), afunilando até uma base plana de x 4,5 a 15,5 em y = 30,75. Faixas de bruma em y = 18,8 (x 4,6 a 13,8) e y = 23,6 (x 7,2 a 15,4), dentro do contorno. Caixa externa do traço: x 0,25 a 19,75; y 1,25 a 31,5. Espaço entre símbolo e nome: ~6,25 (da borda externa do vaso, x 19,75, à borda externa do "A"/"B", x 26). Ícone: mesma silhueta preenchida, centrada em x = 16 (largura máxima 19,6; base 12,4; y 2 a 30,5), faixas vazadas.
- Largura total: 81 (o último traço do "a" termina em x = 79,85 + 0,75 de meio traço).
- Área de proteção: 1/2 da altura do lockup (16 px a 32 px) em todos os lados no uso livre. No header, a área de toque (§4.4) ocupa esse papel na vertical.
- Tamanho mínimo: **32 px de altura** para o lockup (valor exigido pelo handoff; abaixo disso não usar o lockup, usar o ícone). Ícone: 16 px é o mínimo proposto (não testado).
- Proibido: alterar proporção, trocar cor fora das versões previstas, aplicar sombra, contorno ou gradiente, girar, colocar sobre foto sem fundo sólido, usar a faixa de bruma isolada como selo.

## 4. Checagem dos 7 requisitos do `handoff-ui.md` §3

Legenda de evidência: **PROJETO** = atendido por especificação/cálculo; **A CONFIRMAR** = precisa de render e medição reais por QA/Quality.

### 4.1 Legibilidade a 32 px de altura (320 e 375 px) sem quebrar a navegação
- Lockup: 81 × 32 px. x-height externa ~8,5 px (7,0 de linha de centro + 1,5 de traço); espaço livre entre hastes vizinhas ≥ 2,1 px; ascendente e maiúsculas 12 a 13 px.
- Orçamento de largura (estimativa; **A CONFIRMAR** com medição, pois depende das métricas da fonte final):

| Viewport | Padding lateral do header | Logo | Espaço | Sobra para a nav | Nav estimada (3 links) |
|---|---|---|---|---|---|
| 320 | 12 + 12 | 81 (+8 de padding da área de toque = 89) | 8 | 320 − 24 − 89 − 8 = **199** | fonte 13 px/600, padding-inline 4 px: texto ~158 + 24 = ~**182** (folga ~17; com 6 px seria ~194, folga ~5) |
| 375 | 18,75 + 18,75 (5vw) | 81 (+8 = 89) | 12 | 375 − 37,5 − 89 − 12 = **236,5** | fonte 14 px/500, padding-inline 8 px: texto ~170 + 48 = ~**218** |

  A estimativa usa ~0,53 a 0,55 em de largura média por caractere para a sans de UI. Se a medição real estourar, a rede de segurança é `flex-wrap: wrap` (a navegação cai para uma segunda linha; nunca rolagem horizontal) e a UI deve ser avisada. Os links não viram hambúrguer.
- Os traços do wordmark têm 1,5 px: com antialiasing, risco de "afinar demais" em telas 1x. **A CONFIRMAR** em 1x e 2x/3x. Se falhar, a mitigação já estudada é subir o traço do wordmark para 1,75 (reduz o espaço livre entre hastes para ~1,85) e reexportar. Esta é a principal incerteza da proposta.
- Status: **PROJETO / A CONFIRMAR**.

### 4.2 Versão monocromática e contraste
- `logo-mono-fundo-claro.svg` (`#25231F`) e `logo-mono-fundo-escuro.svg` (`#F4F1EC`). Contrastes **calculados à mão** pelo autor (fórmula WCAG de luminância relativa) e **conferidos por script pela revisão independente** (`evidence/UI-001/contrast-check.json`; pares C1, C1b, C1c, C4, C5, C5b, C10 conferem, diferença máxima 0,04):

| Uso | Cor do logotipo / fundo | Razão | Mínimo | Resultado |
|---|---|---|---|---|
| Mono claro sobre canvas | `#25231F` / `#F4F1EC` | 13,92:1 | 3:1 (gráfico) | passa (script) |
| Mono claro sobre surface | `#25231F` / `#EAE6DF` | 12,61:1 | 3:1 | passa (script) |
| Mono claro sobre chip/hover ativo | `#25231F` / `#D9D4CB` | 10,63:1 | 3:1 | passa (script) |
| Mono escuro sobre rodapé | `#F4F1EC` / `#25231F` | 13,92:1 | 3:1 | passa (script) |
| Principal: faixas de argila sobre canvas | `#8A3F22` / `#F4F1EC` | 6,62:1 | 3:1 | passa (script) |
| Principal: faixas de argila sobre hover (surface) | `#8A3F22` / `#EAE6DF` | 6,00:1 | 3:1 | passa (script) |
| Principal: faixas de argila sobre ativo | `#8A3F22` / `#D9D4CB` | 5,06:1 | 3:1 | passa (script) |

  O wordmark é texto desenhado em forma de path; tratado como texto: todos os pares acima também superam 4,5:1. (Logotipos são isentos de WCAG 1.4.3, mas o handoff pediu a verificação; ela foi feita.) Em escala de cinza/monocromática as duas faixas de bruma continuam distinguíveis porque são **interrupções geométricas** dentro do vaso e não dependem de cor. Status: **razões conferidas por script (revisão independente)**; legibilidade visual do símbolo **não avaliada**.

### 4.3 Nome acessível "Ateliê Bruma"
- Marcação recomendada (ver `ui-handoff.md` §5.1):
  ```html
  <a class="brand" href="#topo">
    <img src="logo/logo-principal.svg" width="81" height="32" alt="Ateliê Bruma">
    <span class="sr-only">, início</span>
  </a>
  ```
  Nome acessível do link: **"Ateliê Bruma, início"**: contém o texto visível "Ateliê Bruma" (WCAG 2.5.3), indica o destino e não usa "logotipo" nem "imagem". Os próprios SVGs trazem `role="img"` e `aria-label="Ateliê Bruma"` para uso isolado; no `<img>`, o `alt` é o que vale.
- O nome também aparece em `<title>` da página ("Ateliê Bruma | Cerâmica de mesa feita à mão (marca fictícia)") e no aviso do rodapé ("Ateliê Bruma é uma marca fictícia…"), então o texto do logotipo não é a única forma de acessar a informação.
- Alternativa permitida: SVG inline com `aria-label="Ateliê Bruma, início"` no `<a>` e `aria-hidden="true"` no `<svg>`. Nesse caso o estado "imagem falhou" não existe.
- Status: **PROJETO**; validar com leitor de tela (QA/Quality).

### 4.4 Comportamento: link para `#topo`, alvo de toque, foco
- Link `href="#topo"`. Área clicável: `min-height: 44px; min-width: 44px; padding: 6px 4px` em volta do lockup de 32 px de altura (área final ≈ 89 × 44). Excede o mínimo de 24 × 24 e atende a recomendação de 44 × 44 (a ser medida pelo QA).
- Estados: padrão (sem fundo); hover (fundo `#EAE6DF`, raio 10); ativo (fundo `#D9D4CB`); foco (anel de 3 px `#25231F`, offset 2 px, 13,92:1 contra o canvas, não depende só de cor); a mudança de estado não usa movimento.
- `#topo` é o id do `<header>` (ou do `<body>`); com `scroll-padding-top`, o topo da página não fica coberto pelo header fixo.
- Status: **PROJETO**.

### 4.5 Reflow e imagem que falha
- Arquivo vetorial, sem JS, sem dependências. Tamanho fixo em CSS px (81 × 32), nunca dimensionado em % ou vw; por isso não gera rolagem horizontal de 320 a 1440 px (o lockup ocupa 81 dos 296 px disponíveis a 320). Zoom 200%/400% dobra/quadruplica proporcionalmente; a rede de segurança é o `flex-wrap` do header (§4.1).
- Se o `<img>` falhar, o `alt` "Ateliê Bruma" aparece como texto; estilizar o `<img>` com `font: 600 13px/32px <sans>; color: #25231F; overflow: hidden` para o texto caber nos 81 px (a ~13 px, "Ateliê Bruma" tem ~75 px estimados). Comportamento de `alt` com `width/height` varia entre navegadores: **A CONFIRMAR** (teste com bloqueio de imagens, AC-CON-05).
- Status: **PROJETO / A CONFIRMAR**.

### 4.6 Licença e identidade
- **Criação original** desta tarefa (UI-001). Sem fonte, sem pacote de ícones, sem imagem de terceiros. As letras são geometria própria; os arquivos não embutem nem referenciam fontes. Não há metadados de autoria humana nos SVGs; a titularidade do logotipo fictício não foi definida (pergunta ao proprietário, §6).
- **Sem** elementos da identidade da EIXO (nome, cor, símbolo, tipografia). **Sem** selo, medalha, estrela, coroa de louros ou símbolo que sugira certificação. O vaso é um objeto de produto.
- Status: **ATENDIDO**, salvo a verificação de anterioridade (não feita; marca fictícia).

### 4.7 Entrega
- Principal, monocromáticas (claro e escuro), ícone (claro e escuro) e esta justificativa: entregues em `docs/ui/logo/`. Todos marcados **FICTÍCIO / NÃO APROVADO** nos comentários dos SVGs e neste README. Status: **ATENDIDO**.

## 5. Direção alternativa de logotipo considerada e descartada
- **Monograma "B" com bojo superior vazado** (bruma dissolvendo o bojo de cima): bonito como ícone, mas o nome "Ateliê Bruma" ficaria só como texto ao lado, e o requisito de legibilidade do nome a 32 px passaria a depender mais do wordmark horizontal (largo demais a 320 px). Descartado.
- **Faixas horizontais cortando um círculo** (efeito "sol" fatiado): visualmente fácil, mas é um clichê visual muito difundido e tem pouca relação com cerâmica. Descartado.

## 6. Perguntas ao proprietário
1. Aprova a direção do símbolo (vaso garrafa de cerâmica + faixas de bruma) ou prefere outro objeto (caneca, tigela)? A caneca é a peça de maior apelo de presente (Pesquisa §3.2, FICTÍCIO).
2. Aceita o nome em duas linhas no header, sabendo que a versão em uma linha só existe como proposta e não foi desenhada?
3. A titularidade/licença do logotipo fictício deve ser registrada em algum lugar (ex.: arquivo LICENSE do repositório)? Hoje não está definida.

## 7. Revisão do símbolo (rodada 2): decisão sobre "frasco de laboratório"

**Crítica recebida** (revisor, a sessão que coordena o piloto; não é o proprietário): o vaso da rodada 1 pode ser lido como frasco de laboratório, por ter gargalo reto e longo sobre corpo esférico.

**Decisão: CONCORDO.** Razões, a partir da geometria da versão anterior (leitura de coordenadas; não houve render):
- O gargalo era um tubo de 5 de largura e ~8 de comprimento (y 1,6 a 9,5), cerca de 1/3 da altura do símbolo, terminando em corte reto, sem lábio.
- O corpo era um semicírculo quase perfeito (arco de raio 9,25) com fundo redondo, sem base. Gargalo longo + corpo esférico + fundo redondo + contorno sem borda é a silhueta de um balão volumétrico ou balão de fundo redondo.
- Os traços de cerâmica que faltavam: borda/lábio, ombro, pé ou base plana. Sem eles, nada no desenho dizia "objeto de mesa feito em torno". As faixas de bruma, em vez de reforçarem a leitura, lembravam marcas de graduação de um recipiente de medida, o que piora o risco.

**O que mudou** (todos os 5 SVGs e o `preview.html`; o `viewBox`, a posição do nome e a altura de 32 px não mudaram):
1. Gargalo mais curto: ~3,6 de comprimento (y 4,6 a 8,2), contra ~7,9.
2. Lábio: barra de 6,8 de largura no topo, mais larga que o gargalo (4), com 1,6 de altura e transição diagonal. Isso dá a borda de uma peça torneada.
3. Ombro marcado: curva em S do gargalo ao corpo, em vez do alargamento suave de antes.
4. Base plana: o corpo afunila para um pé de 11 de largura, assentado na linha de base do nome (y = 30,75).
5. Corpo ovoide (largura máxima 18 em y = 17, com a massa mais acima do centro), em vez de esfera.
6. Faixas de bruma e demais letras: inalteradas. Largura total continua 81; o nome não se moveu.

**Limites desta decisão:**
- Continua sem avaliação visual (a revisão renderizou os SVGs só para medir tamanho e carregamento). A nova silhueta é **projeção**: pode ainda parecer garrafa genérica ou frasco, ou ficar com o gargalo fino demais a 32 px (o gargalo tem 4 de largura, 2,5 livres de miolo). Quem revisar deve ver a 32, 64 e 128 px, em 1x e 2x.
- As faixas de bruma ainda podem ser lidas como graduação. Se isso persistir após o render, a alternativa é tirá-las do contorno e mantê-las apenas no ícone preenchido, ou deslocá-las para fora do corpo. Não foi feito por falta de evidência visual.
- A leitura "vaso de cerâmica" e não "frasco" é opinião de projeto, não resultado de teste com pessoas. Sugestão barata de teste: mostrar o símbolo isolado a 5 pessoas e perguntar "o que é?" (HIPÓTESE; não executado).
- Os requisitos 1 a 7 de §4 continuam válidos com as mesmas razões de contraste: as cores não mudaram.
