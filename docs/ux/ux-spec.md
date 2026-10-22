# UX Spec — Landing page Ateliê Bruma

**Task:** UX-001 (issue #3) · **Projeto:** piloto-01 · **DNA:** v0.2.0 (APPROVED somente como briefing fictício)
**Status deste documento:** READY_FOR_REVIEW (não aprovado; UX e UI continuam sem aprovação humana)
**Autor:** eixo-ux-architect · **Data:** 2026-10-22
**Entrada principal:** `docs/ux/research/pesquisa-mercado.md` (citada abaixo como "Pesquisa §x")

> Legenda: **[FATO]** fonte externa citada na pesquisa · **[HIPÓTESE]** inferência a validar · **[FICTÍCIO]** inventado para o piloto · **[DECISÃO]** proposta de UX, sujeita a aprovação.
> Não há pesquisa primária, entrevistas, analytics nem testes com usuários. Nada aqui os substitui (Pesquisa §5).

---

## 1. Enquadramento

| Item | Conteúdo | Tipo |
|---|---|---|
| Problema | Visitante vindo de rede social precisa entender em segundos o que é o Ateliê, ver as peças com preço de referência e saber como/onde encontrá-las. | HIPÓTESE (Pesquisa §2.1) |
| JTBD | "Quando chego por um link do Instagram, quero ver rápido se estas peças servem de presente ou para minha mesa e se posso confiar na qualidade, para decidir se entro em contato ou procuro o ateliê na feira." | HIPÓTESE |
| Público primário | Mulheres 25 a 44 anos, classes B/C, ensino superior, compram para presentear (53%) ou decorar (47%). | FATO (Sebrae/RJ, Pesquisa §1.1) aplicado ao cliente fictício; a adequação à marca é HIPÓTESE |
| Contexto de uso | Celular, vindo de rede social (60% descobrem novidades ali); decisão 55% emocional. | FATO + HIPÓTESE |
| Objetivo da página | Levar o visitante da proposta à coleção e à seção de contato. Não vende. | DNA |
| CTA único | "Conhecer a coleção" → `#colecao` (navegação local). | DNA, restrição |
| Fora de escopo | E-commerce, checkout, pagamento, WhatsApp, formulário com envio, dados reais, deploy, integrações. | DNA |
| Barreiras de compra a endereçar | Acabamento/qualidade 39%, preço alto 27%. | FATO (Pesquisa §1.1) |

### Princípios de conteúdo derivados da pesquisa [DECISÃO]
1. **Prova por processo, não por elogio.** Sem depoimentos nem avaliações (DNA proíbe inventar; os quatro sites de referência também não os usam como prova principal, Pesquisa §1.3). A confiança vem de material, cuidados e prazos.
2. **Preço de referência visível** em cada peça (Pesquisa §2.3). É informativo, sem botão de compra.
3. **Presente como caso de uso nº 1**, com uma sugestão de combinação (Pesquisa §3.2).
4. **Contato diz onde encontrar**, não só como escrever (80% compram presencialmente, Pesquisa §2.5).

---

## 2. Jornada

### 2.1 P0 (DNA): entender a proposta → explorar a coleção → localizar o contato

| Passo | Objetivo do usuário | Elemento de UI | Saída esperada |
|---|---|---|---|
| 1. Chegada | Saber o que é e se interessa | Header + Hero (título, subtítulo, CTA) na primeira tela | Entende "cerâmica de mesa feita à mão" sem rolar |
| 2. Ação primária | Ver as peças | CTA "Conhecer a coleção" (toque único) | Foco e rolagem para `#colecao` |
| 3. Explorar | Comparar peças e preços | 6 cartões com nome, medida, preço de referência | Identifica ao menos uma peça de interesse |
| 4. Confiar | Resolver dúvida de qualidade | Seção "Material e cuidados" | Sabe se vai ao micro-ondas/lava-louças |
| 5. Contato | Saber onde/como falar | Link "Contato" no header (1 toque de qualquer ponto) ou rolagem | Vê e-mail em texto, cidade, feira, prazo de encomenda |
| 6. Fim | Copiar ou clicar no e-mail | `mailto:` com domínio `.example` | Ação concluída (não envia nada pelo site) |

### 2.2 Fluxos alternativos
- **A. Quer contato direto:** chega, toca "Contato" no header, vai a `#contato`. Não passa pela coleção. Suportado.
- **B. Rola sem tocar:** lê na ordem natural (hero → manifesto → coleção → material → contato). A ordem das seções reconta a jornada P0, então a rolagem também a cumpre.
- **C. Link profundo:** abre a URL com `#colecao` ou `#contato`. A seção alvo aparece com o título visível (não coberto pelo header fixo).
- **D. Voltar ao topo:** link "Voltar ao início" no rodapé (e o logotipo no header leva a `#topo`).
- **E. Teclado/leitor de tela:** "Pular para o conteúdo" como primeiro foco; navegação por landmarks e títulos.
- **F. Sem JavaScript:** todo o conteúdo e todas as âncoras funcionam (ver §6.4).
- **G. Clica no e-mail sem cliente de e-mail configurado:** o endereço está em texto visível e selecionável; o `mailto:` é só conveniência (§6.6).

### 2.3 Fluxos de erro
Não há formulário, busca nem envio, portanto não há erros de validação. Os pontos de falha reais são: imagem não carrega, âncora inexistente, JS desligado e `mailto:` sem cliente de e-mail. Tratados em §6.

---

## 3. Arquitetura de informação

### 3.1 Mapa (página única)

```
/  (landing, uma página)
├─ #topo        Header: marca · nav: Coleção · Material · Contato
├─ #proposta    Hero: proposta de valor + CTA "Conhecer a coleção"
├─ #manifesto   Manifesto curto (3 pontos)
├─ #colecao     Coleção "Névoa" (6 peças) + sugestão de presente
├─ #material    Material e cuidados + encomendas
├─ #contato     Contato demonstrativo (texto)
└─ rodapé       Aviso "marca fictícia / dados de exemplo" · voltar ao início
```

### 3.2 Ordem das seções e justificativa [DECISÃO]

| # | Seção | Por que nesta posição | Base |
|---|---|---|---|
| 1 | Header | Orientação e acesso a Contato em 1 toque | Meta Pesquisa §4.2 |
| 2 | Hero | Proposta + CTA na primeira tela de 375 × 667 | Pesquisa §2.1, §4.2 |
| 3 | Manifesto | Responde "quem faz e por quê" em 3 linhas antes de pedir atenção às peças; sustenta a emoção (decisão 55% emocional) | FATO + HIPÓTESE |
| 4 | Coleção | Conteúdo central da jornada P0; destino do CTA | DNA |
| 5 | Material e cuidados | Vem depois de ver as peças, quando surge a dúvida "aguenta o uso?"; ataca a barreira nº 1 (39%) | Pesquisa §1.3 (AMME), §2.2 |
| 6 | Contato | Fecha a jornada; inclui feira e prazo | Pesquisa §2.5 |
| 7 | Rodapé | Transparência do caráter fictício | DNA |

**[DECIDIDO pelo proprietário, 2026-10-22]:** o CTA "Conhecer a coleção" salta o Manifesto e vai direto à Coleção (`#colecao`). Decisão aceita; não é mais variante nem pendência. Racional: o hero já carrega a proposta, então o salto não deixa o visitante sem contexto [HIPÓTESE, não testada com pessoas]. O Manifesto continua acessível por rolagem.

### 3.3 Navegação [DECISÃO]
- Header com o **logotipo** do Ateliê Bruma (proposto por UI-001, decisão do proprietário de 2026-10-22; link para `#topo`; requisitos funcionais em `handoff-ui.md` §3: legível a 32 px de altura no mobile, versão monocromática, nome acessível "Ateliê Bruma") e 3 links: **Coleção**, **Material**, **Contato**. Os links do header são navegação, não CTA; o único elemento com papel de CTA primário é o botão "Conhecer a coleção" no hero. UI não deve criar um segundo botão primário.
- Header fixo (sticky) é permitido, pois garante "Contato em 1 toque de qualquer seção" (Pesquisa §4.2). Se fixo, exige `scroll-margin-top` nas seções alvo e foco não obscurecido (WCAG 2.4.11).
- Menu hambúrguer: **evitar**. São 3 links curtos e cabem em uma linha a 320 px. Se UI julgar que não cabem, deve manter os links visíveis (ex.: duas linhas) e justificar.
- Rótulos: "Coleção" no header e "Conhecer a coleção" no CTA apontam ao mesmo destino. Consistência intencional.

---

## 4. Wireframes textuais

Notação: `[ ]` bloco; `(CTA)` elemento interativo; `▒` placeholder de imagem. Sem decisão de cor, tipografia ou estilo (UI-001).

### 4.1 Mobile first (320 a 767 px), coluna única

```
┌────────────────────────────┐
│ [Skip link: Pular p/ conteúdo]  (visível só no foco)
│ HEADER                      │
│ [logotipo Ateliê Bruma, 32 px] Coleção Material Contato │
├────────────────────────────┤
│ HERO  #proposta             │
│ h1  Cerâmica de mesa feita à mão │
│ p   Uma fornada por mês, para usar todo dia sem medo. │
│ (CTA) Conhecer a coleção    │  <- visível sem rolar em 375x667
│ ▒ imagem hero (placeholder) │
│ etiqueta: marca fictícia    │
├────────────────────────────┤
│ MANIFESTO #manifesto        │
│ h2 + 3 itens curtos (lista) │
├────────────────────────────┤
│ COLEÇÃO #colecao            │
│ h2 Coleção Névoa            │
│ p  intro + etiqueta "preços de exemplo" │
│ ┌ Cartão peça 1 ┐           │
│ │ ▒ imagem      │           │
│ │ h3 Caneca Névoa │         │
│ │ 300 ml        │           │
│ │ R$ 98 (exemplo) │         │
│ └───────────────┘ x6, empilhados, 1 coluna │
│ Sugestão de presente (texto)│
├────────────────────────────┤
│ MATERIAL #material          │
│ h2 + lista de cuidados + encomendas │
├────────────────────────────┤
│ CONTATO #contato            │
│ h2 Contato  + etiqueta "dados de exemplo" │
│ E-mail (texto + mailto)     │
│ Endereço · Cidade · Feira · Encomendas │
├────────────────────────────┤
│ FOOTER: aviso fictício · Voltar ao início │
└────────────────────────────┘
```

Regras mobile:
- 1 coluna; sem rolagem horizontal de 320 a 767 px.
- Cartões de peça: ordem interna imagem → nome → medida → preço. Tudo visível sem abrir, expandir ou passar o mouse (Pesquisa §4.2).
- Alvos de toque: mínimo 24 × 24 CSS px (WCAG 2.5.8); recomendado 44 × 44 para header, CTA e `mailto:`.
- Texto base legível sem zoom; reflow a 320 px (WCAG 1.4.10).

### 4.2 Desktop (≥ 1024 px)

```
┌──────────────────────────────────────────────────────┐
│ [logotipo Ateliê Bruma]           Coleção  Material  Contato │
├──────────────────────────────────────────────────────┤
│ HERO (2 colunas)                                     │
│ [h1 · subtítulo · (CTA)]            [▒ imagem hero]  │
├──────────────────────────────────────────────────────┤
│ MANIFESTO: h2 à esquerda | 3 itens à direita         │
├──────────────────────────────────────────────────────┤
│ COLEÇÃO: h2 + intro                                  │
│ grade 3 x 2: [peça][peça][peça] / [peça][peça][peça] │
│ Sugestão de presente (faixa de texto)                │
├──────────────────────────────────────────────────────┤
│ MATERIAL: 2 colunas (cuidados | encomendas)          │
├──────────────────────────────────────────────────────┤
│ CONTATO: bloco de texto, largura de leitura limitada │
├──────────────────────────────────────────────────────┤
│ FOOTER                                               │
└──────────────────────────────────────────────────────┘
```

Tablet (768 a 1023 px): grade da coleção em 2 colunas (3 linhas). Largura máxima do conteúdo e comprimento de linha ficam com UI, com o limite funcional de não haver overflow horizontal de 320 a 1440 px.

---

## 5. Hierarquia semântica exigida [DECISÃO]

- Landmarks: `header`, `nav` (com nome acessível, ex.: "Principal"), `main`, `footer`. Seções com `aria-labelledby` apontando para o `h2`.
- Um único `h1` (hero). `h2` por seção. `h3` por peça.
- Coleção como lista (`ul`/`li`) de 6 itens, para que leitores de tela anunciem "lista de 6 itens".
- Dados de contato em texto real (não em imagem).
- `lang="pt-BR"` no documento.

---

## 6. Estados

### 6.1 Placeholders de imagem
- Não há assets licenciados (`assets_approved: false`). Toda imagem é placeholder: caixa com proporção fixa (evita deslocamento de layout, CLS) e identificação textual "Imagem ilustrativa (placeholder)".
- Cada placeholder informativo tem `alt` descritivo da peça futura (texto em `content-structure.md`). O alt descreve o que a foto mostrará, sem afirmar que é foto real. A etiqueta visível "Imagem ilustrativa" deve existir para não induzir ao erro.
- Placeholder puramente decorativo (se UI criar algum) usa `alt=""`. Imagens da peça não são decorativas, porque o nome e o texto já estão ao lado: o alt de cada peça deve acrescentar a descrição visual, sem repetir o nome palavra por palavra.
- Se a imagem real futura falhar ao carregar: o cartão mantém nome, medida e preço (conteúdo não depende da imagem) e a caixa mantém a proporção.
- Se UI usar `<img>` para o placeholder, exigir `width` e `height` ou `aspect-ratio`. Se usar CSS puro, a descrição deve vir de `role="img"` + `aria-label` ou de texto visível.

### 6.2 Foco e teclado
- Ordem de tabulação = ordem visual: skip link → logotipo → Coleção → Material → Contato → CTA → (links de e-mail) → rodapé.
- Foco visível em todo elemento interativo, com contraste ≥ 3:1 contra o entorno (WCAG 2.4.7, 1.4.11). Estilo do foco: livre para UI.
- Foco não pode ficar oculto por header fixo (WCAG 2.4.11).
- Ao ativar uma âncora (header ou CTA), o foco deve ir para a seção alvo. Se o alvo for `h2`/`section` não focável, usar `tabindex="-1"` no alvo para o foco seguir a rolagem. Sem isso, o próximo Tab volta ao ponto de origem. [DECISÃO, validar com QA]
- Skip link leva a `#conteudo` (início do `main`) e fica visível ao receber foco.

### 6.3 Navegação por âncora
- Alvos: `#topo`, `#proposta`, `#manifesto`, `#colecao`, `#material`, `#contato`. Ids únicos, estáveis, em minúsculas e sem acento, porque o CTA depende de `#colecao`.
- Rolagem suave só se `prefers-reduced-motion: no-preference`; caso contrário, salto imediato (WCAG 2.3.3, boas práticas).
- O título da seção alvo não pode ficar sob o header fixo (`scroll-margin-top`).
- URL atualiza com o hash (comportamento padrão); botão "voltar" do navegador retorna à posição anterior.
- Hash inexistente (ex.: `#xyz`): a página abre no topo, sem erro visível. Aceitável.

### 6.4 Sem JavaScript
- A página é HTML que funciona integralmente sem JS: conteúdo, âncoras, `mailto:`, skip link.
- JS, se usado, apenas para melhorias opcionais (nenhuma é necessária no escopo). Nada de conteúdo renderizado só por JS. Nenhum carrossel.
- Rolagem suave deve ser feita em CSS (`scroll-behavior`), e não em JS.

### 6.5 Vazio / carregamento / sucesso / falha
| Estado | Aplicável? | Tratamento |
|---|---|---|
| Vazio (sem peças) | Não: lista estática de 6 | Se a lista falhar a renderizar, não há fallback dinâmico; é estática |
| Carregamento | Parcial | Imagens com proporção reservada; texto aparece sem esperar imagem |
| Sucesso | Não há envio | Só copiar/abrir e-mail; sem mensagem de "enviado" (não existe envio) |
| Falha de imagem | Sim | §6.1 |
| Falha de `mailto:` | Sim | §6.6 |
| 404 / rotas | Fora de escopo (uma página, sem deploy) | Registrar para Developer apenas se vier a ser publicada |

### 6.6 E-mail de contato
- Mostrar o endereço `contato@ateliebruma.example` em texto visível e selecionável, dentro do link `mailto:`. O texto do link é o próprio endereço (rótulo claro, WCAG 2.4.4).
- O domínio `.example` é reservado (RFC 2606): nada será entregue. Isso é correto para o piloto. A etiqueta "dados de exemplo" fica junto do bloco.
- Sem botão "copiar" que dependa de JS (pode ser omitido). A métrica "copia ou clica" da Pesquisa §4.1 é **fictícia** e não será medida em lugar nenhum (sem analytics no escopo).

### 6.7 Responsividade e zoom
- Reflow sem rolagem horizontal de 320 a 1440 px; zoom 200% e 400% (equivalente a 320 px) sem perda de conteúdo.
- Orientação livre (paisagem e retrato).
- Espaçamento de texto ajustável pelo usuário sem corte (WCAG 1.4.12).

---

## 7. Heurísticas de Nielsen aplicadas (análise de especialista, não teste com usuários)

| Heurística | Aplicação na spec | Risco residual |
|---|---|---|
| 1. Visibilidade do estado do sistema | Hash na URL muda; foco acompanha a âncora; item atual na navegação pode ser indicado (opcional, `aria-current` não obrigatório em landing) | Sem indicador de seção ativa por padrão; aceitável em página curta |
| 2. Correspondência com o mundo real | Linguagem de ateliê e de mesa ("caneca", "fornada", "grés"); preços em R$ | Termo "grés" pode ser desconhecido; explicar numa frase em "Material" |
| 3. Controle e liberdade | "Voltar ao início"; botão voltar funciona; nada irreversível | — |
| 4. Consistência e padrões | CTA e link "Coleção" vão ao mesmo lugar; ordem de seção = ordem de nav | Mínimo |
| 5. Prevenção de erros | Sem formulário; e-mail visível em texto evita depender do `mailto:` | — |
| 6. Reconhecimento em vez de memória | Nome, medida e preço juntos em cada cartão; nada oculto | — |
| 7. Flexibilidade e eficiência | Link direto a Contato; âncoras profundas; skip link | — |
| 8. Estética e design minimalista | 5 seções, 1 CTA, sem carrossel | Risco de página "rala" demais; avaliar com pessoas |
| 9. Ajuda a reconhecer e corrigir erros | Imagem falha → conteúdo continua; sem JS → continua | — |
| 10. Ajuda e documentação | Seção "Material e cuidados" faz o papel de FAQ mínimo | Sem FAQ; HIPÓTESE de que basta |

### Esforço cognitivo e escolha
- Uma decisão por tela: o hero tem uma ação; a coleção tem 6 itens (dentro do limite razoável, sem filtros nem ordenação).
- Sem filtros, busca nem ordenação: 6 peças não justificam.

---

## 8. Dependências e pontos para decisão humana
1. **Aprovação deste UX** (humano). Até lá, UI-001 só pode iniciar como exploração; não tratar como UX aprovado.
2. **A promessa "uma fornada por mês"** e demais promessas operacionais são [FICTÍCIO]; se algum dia virar real, precisa ser validado.
3. **Afirmações técnicas de produto** ("micro-ondas e lava-louças", "~1.240 °C") são [FICTÍCIO] baseadas em AMME (Pesquisa §3.2). Em marca real exigiriam validação do ateliê. Mantidas com a etiqueta "exemplo".
4. **Preços** são [FICTÍCIO], posicionados na faixa [FATO] de Ise, AMME e Cafaz (Pesquisa §1.2). Preços observados em 2026-10-22 e podem mudar.
5. **Cidade Curitiba (PR) e endereço:** a cidade é real. O endereço **"Rua da Bruma Clara, 214, Curitiba (PR)" é FICTÍCIO, inventado por decisão do proprietário (2026-10-22)**, em substituição à omissão prevista na Pesquisa §3.3 (que não é mais a referência para este item). Sem CEP, sem link de mapa, com a etiqueta "dados de exemplo". Risco residual: o endereço pode coincidir com via real; mantido por decisão do proprietário, sempre com a etiqueta. Telefone, WhatsApp e redes sociais continuam proibidos.
6. **Logotipo:** a UI-001 propõe o logotipo (decisão do proprietário, 2026-10-22). O UX define só requisitos funcionais; forma, cor e tipografia ficam com a UI e dependem de aprovação humana.
7. **Dica "Evite choques bruscos de temperatura":** mantida por aceite do proprietário (2026-10-22); continua inferência editorial [FICTÍCIO], não baseada na pesquisa.

## 9. Fontes
- Pesquisa §1.1 (Sebrae/RJ, 2.400 consumidores, jan/2026), §1.2 (Ise, AMME, Cafaz, Ana Rojo), §1.3 (padrões de site), §1.4 (conversão), §2 (implicações), §3 (marca fictícia), §4 (metas), §5 (limites).
- WCAG 2.2 AA (critérios citados no `acceptance-criteria.md`).
- Heurísticas de Nielsen (10).
