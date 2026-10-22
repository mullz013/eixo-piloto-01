# Estrutura de conteúdo — Landing page Ateliê Bruma

**Task:** UX-001 · **DNA:** v0.2.0 (briefing fictício) · **Status:** READY_FOR_REVIEW (copy demonstrativa, não aprovada)
**Base:** `docs/ux/research/pesquisa-mercado.md` ("Pesquisa §x") e `docs/ux/ux-spec.md`.

## Regras gerais
- Idioma: português do Brasil. Tom: direto, caloroso, sem exagero e sem promessa terapêutica ou regulatória.
- **Tudo sobre o Ateliê Bruma é [FICTÍCIO].** Preços, medidas, temperatura, prazos, feira e e-mail levam a etiqueta visível **"exemplo"** (ou "dados de exemplo" no bloco).
- **Sem depoimentos, avaliações, notas, selos, "mais vendido" ou números de vendas.** Sem contagem regressiva ou escassez artificial.
- Sem telefone, WhatsApp, endereço, Instagram, CNPJ.
- Textos entre `{{ }}` são instruções ao desenvolvimento, não copy.
- Etiqueta de caráter fictício: texto visível, não só no código.
- Comprimento: títulos curtos; parágrafos de até ~3 linhas em mobile.

---

## 0. Metadados da página (SEO básico)
| Campo | Texto demonstrativo |
|---|---|
| `<title>` | Ateliê Bruma | Cerâmica de mesa feita à mão (marca fictícia) |
| meta description | Coleção Névoa, 6 peças de cerâmica utilitária em grés, feitas à mão. Página demonstrativa de uma marca fictícia, com dados de exemplo. |
| `lang` | pt-BR |
| Open Graph / imagem social | Não definir imagem (sem asset licenciado) |

---

## 1. Header
- Marca (texto, link para `#topo`): **Ateliê Bruma**
- Skip link: **Pular para o conteúdo**
- Nav (nome acessível "Principal"): **Coleção** (`#colecao`) · **Material** (`#material`) · **Contato** (`#contato`)

## 2. Hero · `#proposta`
Função: responder "o que é isto e serve para mim?" e levar à coleção.

- Etiqueta: **Marca fictícia · página demonstrativa**
- h1: **Cerâmica de mesa feita à mão**
- Subtítulo: **Uma fornada por mês, para usar todo dia sem medo.** *(exemplo)*
- Apoio (1 linha): **Grés de alta temperatura, esmalte fosco e peças que podem ir ao micro-ondas e à lava-louças.** *(exemplo)*
- **CTA (único): Conhecer a coleção** → `#colecao`
- Imagem placeholder (hero)
  - Legenda visível: **Imagem ilustrativa (placeholder)**
  - Alt: **Mesa posta com caneca, xícara com pires e tigela de cerâmica cinza-clara, esmalte fosco, ilustração a ser substituída por foto do ateliê.**

Racional: proposta e prova de uso diário na primeira tela (Pesquisa §2.1, barreira de qualidade 39% em §1.1).

## 3. Manifesto · `#manifesto`
- h2: **Feito devagar, para durar**
- Intro (1 frase): **O Ateliê Bruma é um ateliê de uma ceramista que faz peças de mesa com a calma de quem queima uma fornada por vez.** *(exemplo)*
- Lista (3 itens, cada um com título curto + 1 frase):
  1. **Feito à mão.** Cada peça é modelada e esmaltada no ateliê, sem molde industrial.
  2. **Cada fornada é única.** O esmalte fosco muda de tom de uma peça para outra; a variação é parte do desenho.
  3. **Para o uso de todo dia.** Queima em alta temperatura, pensada para a rotina da cozinha.
- Fonte/racional: transformar variação em valor (Ana Rojo, Pesquisa §1.3); prova por processo (Pesquisa §2.2).
- Nota: "bruma" explica o nome e o conceito verbal. Visual não é definido aqui.
  - Linha opcional: **"Bruma" é névoa: tons suaves, bordas que se diluem.**

## 4. Coleção Névoa · `#colecao`
- h2: **Coleção Névoa**
- Intro: **Seis peças para a mesa do dia a dia. Pensadas também como presente.**
- Etiqueta (visível, perto do título): **Preços de referência de exemplo. Não há venda neste site.**

### Peças (todas [FICTÍCIO]; faixa baseada em Pesquisa §1.2 e §3.2)
Cada cartão mostra: nome (h3), medida, **"R$ X (exemplo)"**, uma frase de uso e placeholder de imagem com legenda "Imagem ilustrativa (placeholder)".

| # | Nome (h3) | Medida | Preço de referência | Frase de uso | Alt do placeholder |
|---|---|---|---|---|---|
| 1 | Caneca Névoa | 300 ml | R$ 98 (exemplo) | Para o café da manhã ou para dar de presente. | Caneca de cerâmica cinza-clara, esmalte fosco, alça arredondada. |
| 2 | Xícara de café com pires | 120 ml | R$ 84 (exemplo) | Um presente de entrada, pequeno e fácil de embalar. | Xícara pequena de cerâmica cinza-clara sobre pires do mesmo esmalte fosco. |
| 3 | Tigela funda | Ø 15 cm · 600 ml | R$ 92 (exemplo) | Sopa, cereal ou salada, no uso diário. | Tigela funda de cerâmica em tom de névoa, esmalte fosco, borda levemente irregular. |
| 4 | Prato raso | Ø 26 cm | R$ 128 (exemplo) | A base da mesa posta. | Prato raso redondo de cerâmica cinza-claro, esmalte fosco, borda fina. |
| 5 | Travessa oval | 32 × 22 cm | R$ 210 (exemplo) | Para servir à mesa. | Travessa oval rasa de cerâmica cinza-clara, esmalte fosco, alças baixas. |
| 6 | Vaso garrafa | altura 22 cm | R$ 186 (exemplo) | Um ramo seco já basta. | Vaso de gargalo estreito em cerâmica cinza-clara, esmalte fosco, corpo arredondado. |

Nota: a frase da travessa não menciona forno, porque a pesquisa (§3.2) só afirma micro-ondas e lava-louças.

### Sugestão de presente (texto, sem botão, sem carrinho)
- h3: **Ideia de presente**
- Texto: **Caneca Névoa + xícara com pires: R$ 182 (exemplo).** Combinação sugerida, não é pacote à venda.
- Racional: valor próximo ao ticket médio R$ 150 (~3 peças) [FATO, Pesquisa §1.1].
- Conferência: 98 + 84 = 182.

### Estados
- Sem imagem: nome, medida e preço permanecem.
- Sem botão "comprar", "adicionar", "ver mais" ou "detalhes".

## 5. Material e cuidados · `#material`
- h2: **Material e cuidados**
- Etiqueta: **Informações de exemplo**
- Bloco 1, h3 **O que é grés**: **Grés é uma argila queimada em temperatura alta, em torno de 1.240 °C, o que deixa a peça resistente e pouco porosa.** *(exemplo; base AMME, Pesquisa §1.3 e §3.2)*
- Bloco 2, h3 **Como cuidar** (lista):
  - Pode ir ao micro-ondas.
  - Pode ir à lava-louças.
  - Evite choques bruscos de temperatura. {{inferência editorial genérica, não consta na pesquisa}}
- Bloco 3, h3 **Cada peça é um pouco diferente**: **O esmalte pode variar de tom entre uma fornada e outra. Isso não é defeito, é o jeito da peça.**
- Bloco 4, h3 **Encomendas**: **Peças sob encomenda levam até 45 dias.** *(exemplo; abaixo dos ~60 dias citados, Pesquisa §1.1)*
- Racional: responde à barreira "qualidade/acabamento" (39%) e "durabilidade" (47%) [FATO, Pesquisa §1.1].
- Sem afirmações de saúde, segurança alimentar certificada ou "atóxico" (exigiriam fonte aprovada).

## 6. Contato · `#contato`
- h2: **Contato**
- Etiqueta (visível): **Dados de exemplo. Este endereço e esta feira não existem.**
- Lista de descrição (rótulo + valor):
  - **E-mail:** `contato@ateliebruma.example` *(link `mailto:`; texto do link = endereço)*
  - **Cidade:** Curitiba (PR). Ateliê aberto com hora marcada.
  - **Onde encontrar as peças:** Feira mensal de cerâmica autoral, todo 2º sábado.
  - **Encomendas:** prazo de até 45 dias.
- Sem formulário, telefone, WhatsApp, endereço ou rede social (Pesquisa §3.3).
- Texto de apoio opcional: **Escreva para saber quais peças da fornada estão disponíveis.** *(não prometer resposta em prazo)*

## 7. Rodapé
- **Ateliê Bruma é uma marca fictícia criada para um piloto de avaliação. Todos os dados desta página são exemplos.**
- Link: **Voltar ao início** (`#topo`)
- Direitos/ano: {{omitir; não há titular real}}
- Sem links externos, sem política de privacidade (não há coleta de dados). {{se a página passar a coletar dados, abrir novo item de UX}}

---

## Mapa de etiquetas "exemplo"
| Onde | Texto da etiqueta |
|---|---|
| Hero | Marca fictícia · página demonstrativa |
| Subtítulo e apoio do hero | (exemplo) |
| Coleção (título) | Preços de referência de exemplo. Não há venda neste site. |
| Cada preço | R$ X (exemplo) |
| Material | Informações de exemplo |
| Contato | Dados de exemplo… |
| Rodapé | Marca fictícia |
| Imagens | Imagem ilustrativa (placeholder) |

## Prioridade de leitura (primeira tela mobile 375 × 667)
1. h1 + subtítulo → 2. CTA → 3. etiqueta fictícia → 4. início da imagem.

## Itens que NÃO existem (conferência para QA)
Depoimentos · avaliações/estrelas · contagem de clientes · selos · "mais vendido" · carrinho · botão comprar · formulário · WhatsApp · telefone · endereço · Instagram · imagens reais ou de banco.

## Pendências de revisão de conteúdo
- Confirmar que "Evite choques bruscos de temperatura" é aceitável como orientação genérica ou removê-la (é inferência, não consta na pesquisa).
