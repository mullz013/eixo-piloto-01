# Critérios de aceite — Landing page Ateliê Bruma

**Task:** UX-001 · **DNA:** v0.2.0 (briefing fictício) · **Status:** APROVADO pelo proprietário em 2026-10-22 (ver handoffs/approval-log.md)
**Base:** `ux-spec.md`, `content-structure.md`, `research/pesquisa-mercado.md` ("Pesquisa §x").
Esses critérios valem para a implementação futura (DEV) e para a validação (QA e Quality). Nenhum foi executado: não há site.

IDs: `AC-P0-*` jornada, `AC-NAV-*` navegação, `AC-CON-*` conteúdo, `AC-A11Y-*` acessibilidade, `AC-RESP-*` responsividade, `AC-PERF-*` desempenho, `AC-SEO-*`.

---

## 1. Cenários Dado/Quando/Então

### Jornada P0
**AC-P0-01 · CTA visível na primeira tela**
- Dado um viewport de 375 × 667 em página recém-carregada, sem rolagem
- Quando observo a primeira tela
- Então vejo o h1, o subtítulo e o botão "Conhecer a coleção" por inteiro, sem rolar.

**AC-P0-02 · CTA leva à coleção**
- Dado a página carregada
- Quando ativo "Conhecer a coleção" com toque, clique ou Enter
- Então a URL passa a terminar em `#colecao`, o título "Coleção Névoa" fica visível (não coberto pelo header) e o foco de teclado está na seção da coleção ou em seu título.

**AC-P0-03 · Cartões completos sem interação**
- Dado que estou na seção Coleção
- Quando olho cada um dos 6 cartões
- Então cada um mostra nome, medida e "R$ X (exemplo)" sem hover, clique ou expansão.

**AC-P0-04 · Contato em 1 toque**
- Dado que estou em qualquer ponto da página
- Quando ativo "Contato" no header
- Então vou a `#contato` com o h2 visível e o e-mail legível; é uma única ativação.

**AC-P0-05 · Contato completo e rotulado**
- Dado que estou em `#contato`
- Quando leio a seção
- Então vejo e-mail `contato@ateliebruma.example`, cidade, feira e prazo de encomenda, mais a etiqueta "Dados de exemplo".

### Navegação e alternativos
**AC-NAV-01 · Skip link**
- Dado a página carregada
- Quando pressiono Tab uma vez
- Então o primeiro foco é "Pular para o conteúdo", visível, e Enter move o foco ao início do `main`.

**AC-NAV-02 · Link profundo**
- Dado que abro a URL com `#contato` (e separadamente com `#colecao`)
- Quando a página carrega
- Então a seção alvo aparece com o título visível, sem ficar sob o header fixo.

**AC-NAV-03 · Voltar do navegador**
- Dado que ativei uma âncora
- Quando uso "voltar" do navegador
- Então retorno à posição anterior e a página não recarrega com perda de contexto.

**AC-NAV-04 · Foco não perdido**
- Dado que ativei uma âncora com teclado
- Quando pressiono Tab
- Então o foco segue a partir da seção alvo, não do link de origem.

**AC-NAV-05 · Sem JavaScript**
- Dado o JavaScript desabilitado
- Quando percorro a página, uso o CTA, os links do header, o skip link e o `mailto:`
- Então todo o conteúdo e todas as âncoras funcionam.

**AC-NAV-06 · Movimento reduzido**
- Dado `prefers-reduced-motion: reduce`
- Quando ativo uma âncora
- Então a rolagem é imediata, sem animação.

**AC-NAV-07 · Hash inexistente**
- Dado a URL com `#naoexiste`
- Quando a página carrega
- Então abre normalmente no topo, sem erro visível.

**AC-NAV-08 · Voltar ao início**
- Dado que estou no rodapé
- Quando ativo "Voltar ao início" (ou o logotipo no header)
- Então vou a `#topo`.

### Conteúdo e estados
**AC-CON-01 · Etiquetas "exemplo"**
- Dado a página renderizada
- Quando listo todo preço, medida técnica, temperatura, prazo, feira, endereço, e-mail e cidade
- Então cada um tem etiqueta "exemplo" ou "dados de exemplo" visível no próprio item ou no bloco, conforme `content-structure.md` (Mapa de etiquetas).

**AC-CON-02 · Sem prova social inventada**
- Dado a página renderizada
- Quando busco depoimentos, notas, estrelas, contagens de clientes, selos ou "mais vendido"
- Então não existe nenhum.

**AC-CON-03 · Sem funções fora de escopo**
- Dado o HTML final
- Quando busco `<form>`, botão comprar/carrinho, links `wa.me`/WhatsApp, telefone, CEP, link ou embed de mapa, @ de rede social, scripts de analytics ou de terceiros
- Então não há nenhum.
- E quando busco endereço físico, o único permitido é o fictício "Rua da Bruma Clara, 214, Curitiba (PR)" no bloco Contato, em texto simples, com a etiqueta "dados de exemplo" (decisão do proprietário, 2026-10-22; substitui a omissão da Pesquisa §3.3). Qualquer outro endereço reprova.

**AC-CON-08 · Endereço fictício**
- Dado o bloco Contato
- Quando leio o endereço
- Então aparece "Rua da Bruma Clara, 214, Curitiba (PR)", sem CEP, não é link (nem mapa), e a etiqueta "Dados de exemplo. Este endereço e esta feira não existem." está visível no mesmo bloco.

**AC-NAV-09 · Logotipo no header** *(requisitos funcionais; forma, cor e tipografia ficam com UI-001)*
- Dado o header em 320 e 375 px de largura
- Quando inspeciono o logotipo
- Então ele tem 32 px de altura e continua legível, é um link para `#topo`, tem nome acessível que contém "Ateliê Bruma" (alt ou `aria-label`, sem "logotipo"/"imagem"), foco visível, alvo ≥ 24 × 24 px (recomendado 44), não causa rolagem horizontal, os 3 links de navegação continuam visíveis, e existe uma versão monocromática legível com contraste ≥ 3:1 (WCAG 1.4.11; texto conforme 1.4.3).

**AC-CON-04 · Placeholders honestos**
- Dado cada imagem
- Quando inspeciono
- Então mostra a legenda "Imagem ilustrativa (placeholder)", tem alt descritivo conforme `content-structure.md` e proporção reservada. Nenhum arquivo de imagem tem origem sem licença documentada.

**AC-CON-05 · Falha de imagem**
- Dado que bloqueio o carregamento das imagens
- Quando abro a página
- Então nome, medida, preço e todos os textos permanecem legíveis e o layout não quebra.

**AC-CON-06 · E-mail utilizável sem cliente de e-mail**
- Dado um dispositivo sem cliente de e-mail configurado
- Quando ativo o link de e-mail e nada abre
- Então o endereço continua visível e selecionável para cópia manual.

**AC-CON-07 · CTA único**
- Dado a página
- Quando conto elementos com papel de ação primária
- Então há exatamente um: "Conhecer a coleção". Os links do header são navegação.

---

## 2. Metas mensuráveis

Origem: Pesquisa §4.2 (metas testáveis). As metas de funil (§4.1) são **[FICTÍCIO]** e **não são verificáveis** (sem analytics, sem tráfego). Ficam apenas como referência para decisões de layout.

| ID | Meta | Método | Tipo |
|---|---|---|---|
| M1 | CTA visível sem rolagem em 375 × 667 | Teste em navegador, viewport emulado | Verificável (QA) |
| M2 | CTA → `#colecao` em 1 ativação | Teste automatizado + manual | Verificável |
| M3 | "Contato" alcançável em 1 ativação de qualquer ponto | Teste manual | Verificável |
| M4 | 6/6 cartões com nome, medida e preço visíveis | Inspeção DOM + visual | Verificável |
| M5 | Zero overflow horizontal de 320 a 1440 px | Teste em larguras 320, 375, 768, 1024, 1440 | Verificável |
| M6 | Alvos de toque ≥ 24 × 24 px (mínimo); 44 × 44 recomendado para CTA, header, e-mail | Medição de bounding box | Verificável |
| M7 | Contraste de texto ≥ 4,5:1 (texto grande ≥ 3:1) e componentes/foco ≥ 3:1 | Ferramenta de contraste | Verificável |
| M8 | LCP ≤ 2,5 s em 4G simulado | Lighthouse ou equivalente, mediana de várias execuções | Verificável (aferição em laboratório, não em campo) |
| M9 | CLS ≤ 0,1 | Lighthouse ou equivalente | Verificável |
| M10 | 100% dos dados fictícios com etiqueta "exemplo" | Inspeção (AC-CON-01) | Verificável |
| M11 | 0 depoimentos/avaliações | Inspeção (AC-CON-02) | Verificável |
| M12 | 0 violações automáticas críticas/sérias de acessibilidade (axe ou equivalente) | Ferramenta automática | Verificável, mas insuficiente sozinha |
| F1 | Funil fictício: 30% clicam no CTA, 25% chegam ao contato, 2% usam o e-mail (Pesquisa §4.1) | — | **Não verificável; só referência** |

Observação: M8 e M9 dependem da stack; o Developer informa o que foi medido e como.

---

## 3. Critérios WCAG 2.2 AA aplicáveis

Aplicáveis a esta página; critérios sem objeto (vídeo, áudio, formulário, captcha, tempo limite) estão em "Não aplicáveis".

| WCAG | Critério | Aplicação na página |
|---|---|---|
| 1.1.1 Conteúdo não textual (A) | Alt em placeholders conforme `content-structure.md`; decorativos com alt vazio |
| 1.3.1 Informações e relações (A) | Landmarks, h1 → h2 → h3, lista de peças em `ul`, lista de descrição no contato |
| 1.3.2 Sequência significativa (A) | Ordem do DOM = ordem visual/leitura |
| 1.3.4 Orientação (AA) | Funciona em retrato e paisagem |
| 1.3.5 Finalidade da entrada (AA) | N/A sem campos (ver abaixo) |
| 1.4.1 Uso de cor (A) | Etiquetas "exemplo" e links não dependem só de cor |
| 1.4.3 Contraste mínimo (AA) | 4,5:1 texto; 3:1 texto grande |
| 1.4.4 Redimensionar texto (AA) | 200% sem perda |
| 1.4.5 Texto em imagens (AA) | Nenhum texto essencial em imagem |
| 1.4.10 Reflow (AA) | 320 px sem rolagem horizontal |
| 1.4.11 Contraste não textual (AA) | Foco, bordas de controles 3:1 |
| 1.4.12 Espaçamento de texto (AA) | Sem corte ao aumentar espaçamento |
| 1.4.13 Conteúdo em hover/foco (AA) | Se houver tooltip/hover, é dispensável e persistente; ideal é não ter |
| 2.1.1 Teclado (A) | Tudo operável por teclado |
| 2.1.2 Sem armadilha de teclado (A) | — |
| 2.4.1 Ignorar blocos (A) | Skip link |
| 2.4.2 Título da página (A) | `<title>` descritivo |
| 2.4.3 Ordem do foco (A) | Conforme `ux-spec.md` §6.2 |
| 2.4.4 Finalidade do link (A) | Rótulos claros, e-mail como texto do link |
| 2.4.6 Cabeçalhos e rótulos (AA) | Títulos descritivos |
| 2.4.7 Foco visível (AA) | Em todo interativo |
| 2.4.11 Foco não obscurecido, mínimo (AA, 2.2) | Header fixo não cobre o elemento focado |
| 2.5.3 Rótulo no nome (A) | Nome acessível contém o texto visível do botão/link |
| 2.5.8 Tamanho do alvo, mínimo (AA, 2.2) | ≥ 24 × 24 px |
| 2.3.3 Animação por interação (AAA) | Adotado como boa prática (rolagem sob `prefers-reduced-motion`) |
| 3.1.1 Idioma da página (A) | `lang="pt-BR"` |
| 3.2.1 / 3.2.2 Em foco / Em entrada (A) | Nada muda de contexto sem ação do usuário |
| 3.2.3 Navegação consistente (AA) | Header igual em toda a página |
| 3.2.6 Ajuda consistente (A, 2.2) | N/A (sem mecanismo de ajuda) |
| 4.1.2 Nome, função, valor (A) | Nav com nome; sem ARIA desnecessário |

**Não aplicáveis (sem objeto):** 1.2.x (mídia), 2.2.x (tempo limite), 2.5.7 Movimento de arrastar, 3.3.x (entrada de dados/erros), 3.3.7 Entrada redundante, 3.3.8 Autenticação acessível, 2.4.5 Várias formas (página única, dispensado para conjunto de uma página).

**Limite:** conformidade WCAG não se declara apenas com ferramenta automática. Declarar "conforme" exige revisão manual (teclado, leitor de tela, zoom). Esta spec não afirma conformidade; define critérios.

---

## 4. Requisitos para QA Engineer (validações técnicas)

1. **Automação funcional** (Playwright ou equivalente): AC-P0-01 a 05, AC-NAV-01 a 08, AC-CON-03, AC-CON-07, M1 a M6.
2. **Viewports:** 320 × 568, 375 × 667, 768 × 1024, 1024 × 768, 1440 × 900. Paisagem em 667 × 375.
3. **Sem JS:** repetir os fluxos com JavaScript desabilitado (AC-NAV-05).
4. **Emulação:** `prefers-reduced-motion: reduce` (AC-NAV-06); bloqueio de imagens (AC-CON-05).
5. **Acessibilidade automática:** axe-core ou Lighthouse a11y nos 5 viewports; reportar 0 violações críticas/sérias (M12) e listar o que ferramenta não cobre.
6. **Desempenho:** Lighthouse com throttling 4G simulado, mediana de ≥ 3 execuções, relatando LCP e CLS (M8, M9). Registrar versão e configuração.
7. **HTML:** validação do markup, ids únicos, `lang`, `<title>`, meta description, landmarks, ordem de headings.
8. **Varredura de conteúdo proibido:** `<form>`, `wa.me`, `whatsapp`, `tel:`, scripts externos, palavras como "depoimento", "avaliação", "estrelas", "mais vendido", arquivos de imagem sem licença (AC-CON-01 a 04).
9. **Evidência:** relatórios, capturas e comandos salvos no repositório (ex.: `evidence/QA-001/`); sem evidência não há "passou".
10. **Gate do piloto:** `python scripts/validate_pilot.py` (ORCH-001) além dos testes acima.
11. QA relata resultado; não aprova UX/UI nem release.

## 5. Requisitos para Quality Specialist (revisão qualitativa)

1. **Revisão manual de teclado** (Tab, Shift+Tab, Enter): ordem, foco visível, foco não obscurecido, skip link (AC-NAV-01, 04).
2. **Leitor de tela** (ex.: NVDA/VoiceOver, um por plataforma disponível): landmarks, títulos, lista de 6 peças, alt dos placeholders, anúncio do contato.
3. **Zoom 200% e 400%** e espaçamento de texto aumentado.
4. **Aderência ao UX:** ordem das seções, CTA único, ausência de dark patterns (escassez, urgência falsa, culpa).
5. **Aderência ao DNA:** fictício assinalado, sem dados reais, sem fora de escopo, sem identidade EIXO.
6. **Revisão de copy:** tom, clareza, afirmações sem base (ex.: "micro-ondas/lava-louças", "1.240 °C", "evite choques bruscos") confirmadas como [FICTÍCIO] e com etiqueta.
7. **Revisão das heurísticas de Nielsen** (`ux-spec.md` §7) contra a implementação.
8. **Regra de honestidade:** análise de especialista não é teste com usuários. O relatório diz isso e não inventa resultados de usabilidade.
9. Quality emite parecer e achados; não altera o código nem aprova release.

---

## 6. Definição de pronto da etapa UX (para o Orchestrator)
- [ ] Os quatro documentos de `docs/ux/` revisados por humano.
- [ ] Decisões em aberto de `ux-spec.md` §8 resolvidas ou aceitas.
- [ ] Aprovação humana registrada pelo Orchestrator (**esta spec não se auto-aprova**).
- [ ] Só depois: UI-001 pode tratar o UX como aprovado.
