# Ateliê Bruma: pesquisa de mercado e base da marca fictícia

**Projeto:** piloto-01 · **DNA:** v0.2.0 (APPROVED só como briefing fictício) · **Data:** 2026-10-22
**Uso:** entrada para UX-001 (eixo-ux-architect). Os dados de mercado vêm de fontes reais, citadas abaixo. Tudo o que descreve o Ateliê Bruma (peças, preços, contato, métricas) é **inventado**, com a justificativa ao lado.

> Legenda: **[FATO]** dado de fonte externa · **[HIPÓTESE]** inferência a partir dos fatos · **[FICTÍCIO]** decisão inventada para o piloto.

---

## 1. O que o mercado diz

### 1.1 Quem compra artesanato no Brasil [FATO]
Pesquisa Sebrae/RJ com 2.400 consumidores, jan/2026 ([Consumidores de artesanato](https://sites.rj.sebrae.com.br/arquivos/crab/Consumidores_de_artesanatos.pdf)):

| Dado | Valor |
|---|---|
| Gênero | 66% mulheres |
| Idade | média 37 anos; 25 a 44 anos é a faixa mais ativa |
| Renda/escolaridade | 39% classes A/B, 45% C; 65% com ensino superior |
| Frequência | média de 4 compras/ano |
| Gasto | R$ 150 por compra em média, ~3 peças; 62% gastam entre R$ 50 e R$ 200 |
| Motivação | presentear 53%, decorar 47% |
| Matéria-prima | argila citada por 30% |
| Canal de compra | 80% presencial (feiras são 60% do presencial), 20% online |
| Descoberta | 60% descobrem novidades em redes sociais, 39% em feiras |
| O que pesa | acabamento (50%), durabilidade (47%), sustentabilidade (42%), economia local (41%) |
| Disposição a pagar mais | 53% pagariam mais por origem/história comprovada (+24% em média) |
| Por que não compram | falta de qualidade/acabamento (39%), preço alto (27%) |
| Decisão | 55% emocional, 45% racional |

Complementos: argila e cerâmica foram 13,8% das vendas principais do 22º Salão do Artesanato, e clientes de cerâmica autoral aceitam esperar ~60 dias por peça sob encomenda (Tita Cerâmica, Taubaté/SP) ([Mais Novela, 21/10/2026, conteúdo patrocinado](https://www.maisnovela.com.br/noticia/tita-ceramica-mostra-crescimento-de-demanda-por-produtos-artesanais-de-alto-padrao-no-brasil.phtml)).

### 1.2 Preços praticados por ateliês brasileiros [FATO]

| Ateliê | Faixa observada | Exemplos |
|---|---|---|
| [Ateliê Ise](https://www.atelieise.com.br/) (utilitária, alta temperatura) | R$ 33 a R$ 155 | copo 180 ml R$ 39,90; caneca 250 ml R$ 99,90; prato 20 cm R$ 45,90; jarra 500 ml R$ 129,90 |
| [AMME Cerâmica](https://www.ammeceramica.com.br/collections/pratos-ceramica-artesanal) (grés de alta temperatura) | R$ 85 a R$ 170 (PIX) | sobremesa R$ 84,55; raso R$ 113,05; risoto R$ 144,40 |
| [Cafaz Ateliê](https://www.cafazatelie.com.br/) (autoral, SP) | R$ 45 a R$ 392 | copo espresso R$ 45; tigela R$ 95; prato raso R$ 139; luminária R$ 392 |
| [Ana Rojo](https://www.anarojo.com.br/) | caneca cheia R$ 60 | discurso "beleza na imperfeição" |

### 1.3 Como esses sites se organizam [FATO → HIPÓTESE]
- **Ise:** navega por *uso* ("para presentear", "para servir", "decorar"). Bate com as motivações do Sebrae (presente 53%, decoração 47%).
- **Cafaz:** organiza por *séries nomeadas* ("Série Vital", "Série Mar") e tem bloco de contato com e-mail, Instagram e endereço.
- **AMME:** explica o material (grés, variações de tom) e os cuidados (micro-ondas, forno, lava-louças). Isso responde à barreira nº 1 (acabamento/durabilidade).
- **Ana Rojo:** transforma imperfeição em valor com uma narrativa curta sobre o processo.
- **Padrão comum:** nenhum dos quatro usa depoimentos como prova principal; a prova é material, processo e origem.

### 1.4 Referências de conversão [FATO]
- E-commerce geral: 2,9% de conversão; mobile 2,8%, desktop 3,2%. Casa e Móveis é o setor que menos converte (1,4%) ([Smart Insights / Dynamic Yield, jan/2025](https://www.smartinsights.com/ecommerce/ecommerce-analytics/ecommerce-conversion-rates/)). A própria fonte tem inconsistências internas; usar só como ordem de grandeza.
- Acessos por aplicativo no e-commerce brasileiro cresceram 10,6% nos 12 meses até nov/2025 ([Mundo do Marketing / Conversion](https://mundodomarketing.com.br/mobile-avanca-dois-digitos-e-reforca-virada-estrutural-no-e-commerce-brasileiro)). Não encontrei participação mobile confiável para Casa e Decoração.

---

## 2. Implicações para a marca e para a UX [HIPÓTESE]

1. **Mobile first de verdade.** O público descobre por redes sociais (60%), então a primeira visita chega quase sempre pelo celular, vindo de um link do Instagram.
2. **A prova é o processo, não o elogio.** Sem depoimentos (o DNA proíbe inventar), a landing deve mostrar material, etapas e cuidados. Isso ataca a barreira de qualidade (39%) e aproveita os 53% que pagam mais por origem.
3. **Mostrar preço de referência.** Preço alto é a 2ª barreira (27%); faixas visíveis evitam que a pessoa saia para perguntar. Não é e-commerce: o preço é informativo.
4. **Presente é o caso de uso nº 1.** A coleção deve ter peças que funcionam sozinhas como presente na faixa R$ 50 a R$ 200.
5. **Contato liga ao canal que o público usa.** 80% compram presencialmente, a maioria em feiras. O contato deve dizer *onde encontrar as peças*, não só como escrever.

---

## 3. Ateliê Bruma [FICTÍCIO]

### 3.1 Posicionamento
- **Quem é:** ateliê de uma ceramista, cerâmica utilitária autoral em grés de alta temperatura, para a mesa do dia a dia.
- **Ideia do nome:** "bruma" (névoa) → peças de esmalte fosco em tons neutros, com variações de fornada assumidas como parte da peça. *Isto é conceito verbal; a direção visual fica com UI/Art Direction (UI-001).*
- **Proposta de valor (rascunho):** "Peças de mesa feitas à mão, uma fornada por mês, para usar todo dia sem medo."
- **Público primário:** mulheres de 25 a 44 anos, classes B/C, com curso superior, que compram para presentear ou montar a própria mesa, e chegam pelo Instagram (base: §1.1).

### 3.2 Coleção demonstrativa "Névoa" (6 peças)
Preços posicionados no meio da faixa observada (§1.2); medidas plausíveis para a categoria.

| Peça | Medida | Preço de referência | Por que existe |
|---|---|---|---|
| Caneca Névoa | 300 ml | R$ 98 | Item de presente individual; mesma faixa da caneca Ise (R$ 99,90) |
| Xícara de café com pires | 120 ml | R$ 84 | Presente de entrada, abaixo do ticket médio |
| Tigela funda | Ø 15 cm, 600 ml | R$ 92 | Uso diário; próxima da tigela Cafaz (R$ 95) |
| Prato raso | Ø 26 cm | R$ 128 | Base da mesa; entre AMME (R$ 113) e Cafaz (R$ 139) |
| Travessa oval | 32 × 22 cm | R$ 210 | Peça de servir; teto da faixa de 62% dos compradores |
| Vaso garrafa | altura 22 cm | R$ 186 | Atende "decoração" (47%) |

Combinação de presente sugerida: caneca + xícara = R$ 182, perto do ticket médio (R$ 150, ~3 peças).
**Material e cuidados (texto demonstrativo):** grés queimado a ~1.240 °C; pode ir a micro-ondas e lava-louças; cada peça varia levemente de tom. Base: AMME (§1.3).
**Imagens:** placeholders com alt descritivo (ex.: "Caneca de cerâmica cinza-clara, esmalte fosco, alça arredondada"). Sem fotos reais ou de banco até haver licença.

### 3.3 Contato demonstrativo
Bloco só de texto, sem formulário (não coleta dados, perfil LITE):
- **E-mail:** `contato@ateliebruma.example` (domínio `.example` é reservado pela RFC 2606 e nunca vai existir, então não aponta para ninguém real).
- **Cidade:** Curitiba (PR), "ateliê aberto com hora marcada". Cidade real. *(Atualização 2026-10-22: a omissão do endereço foi superada por decisão do proprietário, que pediu um endereço inventado: "Rua da Bruma Clara, 214, Curitiba (PR)", sem CEP e sem mapa, com etiqueta "dados de exemplo".)*
- **Onde encontrar as peças:** "Feira mensal de cerâmica autoral, todo 2º sábado" (fictícia). Base: feiras são o principal canal presencial (§1.1).
- **Encomendas:** "prazo de até 45 dias" (abaixo dos ~60 dias citados na §1.1).
- **Sem** telefone, WhatsApp ou @ de Instagram (o endereço fictício acima é exceção por decisão do proprietário), porque poderiam coincidir com pessoas reais. Todo o bloco leva a etiqueta "dados de exemplo".

---

## 4. Métricas fictícias e metas verificáveis

### 4.1 Funil hipotético (para orientar decisões de layout, não é dado real)

| Etapa | Valor fictício | Base |
|---|---|---|
| Visitas/mês | 1.000 | Ateliê pequeno com ~3 mil seguidores (a Tita tem 40 mil) |
| % mobile | 75% | Descoberta por rede social (60%) → tráfego vindo de app |
| Clique no CTA "Conhecer a coleção" | 30% | Única ação primária da página |
| Chegam à seção de contato | 25% | Página curta, 1 tela de contato |
| Copiam o e-mail ou clicam nele | 2% (20/mês) | Acima da compra em Casa e Móveis (1,4%), porque contato custa menos que comprar |

### 4.2 Metas que o QA consegue testar
Formato Dado/Quando/Então; o UX Architect detalha em `acceptance-criteria.md`.
- Em viewport 375 × 667, o CTA "Conhecer a coleção" aparece sem rolagem e leva à âncora `#colecao` em 1 toque.
- A navegação dá acesso a "Contato" em 1 toque a partir de qualquer seção (link fixo ou no topo).
- Cada peça mostra nome, medida e preço de referência sem precisar abrir nada.
- Nenhum overflow horizontal entre 320 px e 1440 px.
- Áreas de toque ≥ 24 × 24 px (WCAG 2.2, 2.5.8), com recomendação de 44 px; contraste de texto ≥ 4,5:1.
- LCP ≤ 2,5 s em perfil 4G simulado (limite "bom" das Core Web Vitals).
- Todo dado fictício visível leva a etiqueta "exemplo"; nenhum depoimento ou avaliação na página.

---

## 5. Limites desta pesquisa
- Os dados de consumidor são de artesanato em geral, não só cerâmica.
- Os preços vêm das páginas iniciais/listagens das lojas em 2026-10-22 e podem mudar.
- Não houve entrevista nem teste com usuários; nada aqui substitui pesquisa primária.
- Fontes com conteúdo patrocinado (Mais Novela) foram usadas só para dados de contexto.
