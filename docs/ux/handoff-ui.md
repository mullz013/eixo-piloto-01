# Handoff UX → UI/Art Direction (UI-001)

**Origem:** UX-001 (eixo-ux-architect) · **Destino:** eixo-ui-art-director · **Projeto:** piloto-01
**DNA:** v0.2.0 (APPROVED somente como briefing fictício) · **Status:** READY_FOR_REVIEW
**Condição:** o UX ainda **não está aprovado** por humano. UI-001 só começa como versão final após aprovação registrada pelo Orchestrator; antes disso, apenas exploração. Esta spec não decide paleta, tipografia nem estilo visual.

## 1. O que você recebe
| Documento | Conteúdo |
|---|---|
| `docs/ux/ux-spec.md` | Enquadramento, jornada, IA, ordem das seções, wireframes textuais, estados, heurísticas |
| `docs/ux/content-structure.md` | Copy demonstrativa por seção, alt dos placeholders, mapa de etiquetas "exemplo" |
| `docs/ux/acceptance-criteria.md` | Cenários, metas (M1 a M12), WCAG 2.2 AA aplicável |
| `docs/ux/research/pesquisa-mercado.md` | Fatos de mercado, marca fictícia, coleção Névoa |

## 2. Objetivos que a UI deve servir
1. Em 375 × 667 sem rolar: h1, subtítulo e CTA "Conhecer a coleção" visíveis.
2. Levar do hero à coleção e ao contato com fricção mínima.
3. Transmitir qualidade por processo e material, sem depoimentos (Pesquisa §2.2).
4. Deixar claro, de forma visível e honesta, que a marca é fictícia e os dados são exemplo.

## 3. Restrições (obrigatórias)
**Estrutura e comportamento**
- Seções e ordem: Header → Hero (`#proposta`) → Manifesto (`#manifesto`) → Coleção (`#colecao`) → Material (`#material`) → Contato (`#contato`) → Rodapé. Ids exatos, em especial `#colecao`.
- **CTA único** "Conhecer a coleção" → `#colecao`. Nenhum segundo botão de ação primária. Links do header são navegação e não devem competir visualmente com o CTA.
- Header com Coleção, Material e Contato **sempre visíveis** (sem hambúrguer, ver `ux-spec.md` §3.3). Se for fixo: tratar `scroll-margin-top`, foco não obscurecido.
- Cartões de peça: nome, medida, preço "(exemplo)" visíveis sem interação. Sem botão comprar, carrinho, ver mais, favoritar, filtros, carrossel.
- Contato é texto; sem formulário, sem campos, sem estados de envio.
- Sem animações que atrasem leitura; qualquer movimento respeita `prefers-reduced-motion`.

**Conteúdo**
- Usar o copy de `content-structure.md`. Mudanças de texto voltam ao UX; a UI pode propor.
- Preservar as etiquetas "exemplo" e a legenda "Imagem ilustrativa (placeholder)" como texto visível, legível e não ocultável.
- Sem depoimentos, estrelas, selos, números de clientes ou "mais vendido", nem como "elemento gráfico".

**Marca e licenças**
- **Não usar a identidade da EIXO** (nome, cores, logotipo, tipografia, tokens).
- Sem assets sem licença: sem fotos de banco, sem fontes com licença incerta, sem ícones de origem desconhecida. Imagens = placeholders. Se a UI propuser fontes ou ícones, informar a licença e a fonte (preferir licenças abertas verificáveis).
- **[DECIDIDO pelo proprietário, 2026-10-22]** UI-001 **deve propor um logotipo** para o Ateliê Bruma (não basta um wordmark em texto). A proposta é FICTÍCIA e **não está aprovada**: forma, cor e tipografia são decisão da UI (§4) e dependem de aprovação humana posterior. Requisitos **funcionais** do logotipo (o UX não decide o desenho):
  1. **Legibilidade em tamanho pequeno:** legível, com o nome "Ateliê Bruma" reconhecível, a **32 px de altura** no header mobile (375 px de largura e também 320 px), sem quebrar a linha de navegação (Coleção, Material, Contato sempre visíveis).
  2. **Versão monocromática** (uma cor sobre fundo claro e/ou escuro) que preserve a legibilidade; a UI deve entregar e testar o contraste (componentes gráficos ≥ 3:1; texto do logotipo, se for texto, ≥ 4,5:1 ou ≥ 3:1 se grande).
  3. **Nome acessível:** o logotipo é o conteúdo do link da marca. Se for imagem/SVG, `alt` (ou `role="img"` + `aria-label`) = **"Ateliê Bruma"**, sem as palavras "logotipo" ou "imagem"; o nome acessível do link deve conter o texto visível do logotipo (WCAG 2.5.3) e indicar o destino (ex.: "Ateliê Bruma, início"). Se o texto do nome estiver dentro da imagem, ele não pode ser a única forma de acessar a informação (o nome também aparece em `<title>` e no aviso do rodapé).
  4. **Comportamento:** o logotipo é um link para `#topo`; alvo de toque recomendado ≥ 44 × 44 px (mínimo 24 × 24), com foco visível.
  5. **Reflow e estado:** sem rolagem horizontal de 320 a 1440 px; se a imagem falhar, o texto alternativo "Ateliê Bruma" permanece. Preferir formato vetorial sem dependência de JS.
  6. **Licença e identidade:** criação original da UI; fontes e ícones usados nele com licença documentada; **sem** elementos da identidade da EIXO e sem selos, medalhas ou símbolos que sugiram certificação.
  7. **Entrega:** arquivos do logotipo (principal, monocromático, ícone/forma reduzida se houver) e justificativa registrados em UI-001, marcados como FICTÍCIO e não aprovados.

**Acessibilidade e responsividade (ver `acceptance-criteria.md` §3)**
- Contraste de texto ≥ 4,5:1 (grande ≥ 3:1); componentes e foco ≥ 3:1.
- Foco visível em todo interativo, sem ser obscurecido pelo header fixo.
- Alvos ≥ 24 × 24 px; recomendado 44 × 44 em header, CTA e e-mail.
- Sem informação só por cor. Sem texto essencial dentro de imagem.
- Reflow de 320 a 1440 px sem rolagem horizontal; zoom de 200%.
- Placeholders com proporção fixa (evita CLS).

## 4. Liberdades (decisão da UI)
- Paleta, tipografia, escala, grid, espaçamento, forma, textura, ícones (licenciados), iconografia, tokens.
- Como o placeholder é desenhado (traço, preenchimento, padrão), desde que a legenda e a proporção existam.
- Estilo do foco, do CTA, do header e dos cartões; microinterações discretas respeitando movimento reduzido.
- Quantidade de colunas por breakpoint (guia: 1 / 2 / 3), largura máxima, ritmo vertical.
- Expressão do conceito "bruma/névoa". O UX só entrega a ideia verbal em `content-structure.md` §3; o visual é de UI-001 e **não está aprovado nem pré-decidido**.
- Propor melhorias ao UX com justificativa (ex.: versão alternativa do hero), em vez de alterar por conta própria.

## 5. Estados que a UI deve desenhar
| Estado | Para |
|---|---|
| Padrão, hover, foco, ativo | CTA, links do header, link do e-mail, "Voltar ao início" |
| Foco visível do skip link | Skip link (aparece ao receber foco) |
| Placeholder de imagem (hero e 6 peças) | Com legenda "Imagem ilustrativa (placeholder)" |
| Imagem falhou | Cartão sem imagem mantendo texto e proporção |
| Etiqueta "exemplo" | Em preços, hero, material, contato (inclui endereço), rodapé |
| Logotipo no header | Padrão, hover, foco, ativo; versão monocromática; 32 px de altura em 320 e 375 px; imagem falhou (alt visível) |
| Seção alvo de âncora | Título não coberto pelo header |
| Largura 320, 375, 768, 1024, 1440 | Todas as seções |

Sem estados de erro de formulário, sucesso de envio, vazio de busca ou carregamento de lista: não existem neste escopo.

## 6. Entregáveis esperados de UI-001 (fora desta tarefa; para alinhar)
Direção de arte própria da marca, tokens, tipografia com licença, especificação de componentes e estados, layouts mobile e desktop, lista de assets e licenças, decisões de contraste verificadas. Aprovação humana antes do Developer.

## 7. Perguntas abertas para o responsável
Nenhuma pergunta aberta. As 4 perguntas da rodada 1 foram respondidas pelo proprietário (Matheus) em 2026-10-22 e estão registradas como **DECIDIDO** (resposta literal: "A logo precisa propor um logotipo. Pode ter o CTA de conhecer a coleção. Pode manter a dica. Invente um endereço."):
1. **Logotipo:** DECIDIDO. A UI propõe um logotipo (§3, Marca e licenças).
2. **CTA "Conhecer a coleção" pulando o Manifesto:** DECIDIDO, aceito. Não é mais variante nem pendência (`ux-spec.md` §3.2). Teste comparativo com pessoas continua sendo uma possibilidade futura, fora de escopo.
3. **Dica "Evite choques bruscos de temperatura":** DECIDIDO, mantida por aceite do proprietário. Continua sendo inferência editorial **FICTÍCIA** (não consta na pesquisa).
4. **Endereço no contato:** DECIDIDO. Endereço fictício "Rua da Bruma Clara, 214, Curitiba (PR)", sem CEP e sem link de mapa, com a etiqueta "dados de exemplo" (`content-structure.md` §6).

Estes registros são decisões do proprietário sobre briefing fictício; **não** equivalem à aprovação do UX nem a APPROVED.

## 8. Fatos x hipóteses x fictício
- **FATO:** dados de consumidor e preços de mercado da pesquisa (com fontes).
- **HIPÓTESE:** que o público-alvo chega por celular via rede social; que preço visível reduz atrito; que a prova por processo basta.
- **FICTÍCIO:** a marca, a coleção, os preços, a cidade, a feira, o e-mail, o endereço (Rua da Bruma Clara, 214, inventado por decisão do proprietário), o prazo, a "fornada mensal" e o logotipo a ser proposto.
- Não houve pesquisa primária, teste de usuário nem aprovação humana do UX.
