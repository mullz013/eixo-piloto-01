# Parecer de QA independente: DEV-002 (loja demonstrativa Ateliê Bruma)

- Projeto: eixo-piloto-01 (marca FICTÍCIA) · DNA 0.2.0 (aprovado só como briefing fictício) · Tarefa: QA-002 · Agente: eixo-qa-engineer
- Commit/branch: não informado na tarefa (`UNAVAILABLE`). Ambiente: nenhum (`none`); análise estática.
- Data: 2026-10-22
- **Veredito: NO-GO** (confiança média; ver seção 6). Os requisitos funcionais do pedido do proprietário estão atendidos pela leitura do código e pelas medições da outra sessão, mas há 1 achado de severidade alta, 1 critério de aceite do UX não atendido (AC-ECOM-06) e evidência visual incompleta.

## 1. Método e limites (leia primeiro)

Este parecer é **revisão estática por leitura**. Eu **não executei** teste, navegador, Playwright, axe, Lighthouse, servidor, script Python nem nenhum comando de verificação, conforme a restrição da tarefa. Divulgação: usei uma única vez `wc -l scripts/gerar_pecas.py` (contagem de linhas, somente leitura, sem efeito no repositório) antes de ler o arquivo. É uma pequena exceção à restrição "não execute comandos" e fica registrada aqui. Nenhum arquivo foi alterado fora de `evidence/DEV-002/qa/`.

Os números de `interaction-check.json` e do `handoffs/DEV-002.md` são **medições da outra sessão (Developer)**. Eu as li e as cruzei com o código, mas não as reproduzi. Onde digo "medido", a fonte é aquela sessão, não eu. Contrastes e larguras citados abaixo são **estimativas manuais minhas**, não saída de ferramenta.

## 2. Requisitos do proprietário x evidência

| Requisito | Situação | Base |
|---|---|---|
| Hambúrguer abaixo de 1024 px | Atende (leitura + medição de terceiros) | styles.css:158, 177-182; json `menu_visible`/`nav_visible` |
| Carrossel desktop: 4 cartões, setas, bullets | Atende | styles.css:43, 395-409; json 1024/1440 = 4 cartões, setas, 2 bullets; captura `vitrine-pagina2-1440.png` |
| Celular: 2 cartões + cerca de 30% do 3º, toque, bullets | Atende por construção: `--card-w` = (100vw - gutter - 2 gap)/2.3 deixa 0,3 do cartão por definição (styles.css:29) | json 320/375 = [1,1,0.3]; captura `vitrine-375.png` |
| Categorias | Atende; contagens 6/3/5/2/4 conferem com o catálogo (total 20) | index.html:103-147; gerar_site.py:32-62 |
| Coleções passadas com vitrines | Atende (Terra Molhada, Sal; 6 peças cada) | index.html:288-485 |
| Sem seção de encomenda nem contato (AC-ECOM-07) | Atende: busca por encomenda/contato/whatsapp/mailto/tel em `site/` sem ocorrências | Grep em site/*.{html,js,css} |
| Banner artístico, rigor estético | Não julgável por QA: é decisão estética do proprietário e do UI/Art Director | capturas `pagina-1440-full.png`, `pagina-375-full.png` |
| Movimento reduzido (AC-ECOM-06: "nenhuma animação roda") | **Não atende** por leitura (QA-02) | styles.css:174-175 |

## 3. Achados

Severidade: bloqueante / alta / média / baixa (dano). Prioridade de correção está separada quando difere. "Origem" = leitura de código, captura, ou medição de terceiros.

| ID | Sev. | Arquivo:linha | Descrição | Correção sugerida |
|---|---|---|---|---|
| QA-01 | **alta** | index.html:37-39; styles.css:165, 194 | O botão da sacola perde o nome acessível abaixo de 1024 px: `.bag-btn__label` ("Sacola") está em `display:none` e o SVG é `aria-hidden`; o nome computado fica só "0" + ", 0 itens" (leitor de tela: "0, 0 itens"). No desktop vira "Sacola 0, 0 itens" (contagem duplicada). Viola WCAG 4.1.2 (A) e 2.4.6. Origem: leitura. | Manter um `<span class="sr-only">Sacola</span>` sempre presente (esconder o rótulo visual com técnica sr-only, não `display:none`) e marcar o badge numérico `aria-hidden`, deixando só ", N itens" para leitores. Nome esperado: "Sacola, 3 itens". |
| QA-02 | média (prioridade alta: critério de aceite) | styles.css:174-175, 209, 351, 419-420, 520; app.js:10 | AC-ECOM-06 ("nenhuma animação roda") não é cumprido: `bump` (420 ms) é animação em `.is-bumped` sem `prefers-reduced-motion`; transições com duração literal (gaveta 280 ms, zoom dos cartões 500/600 ms, barra de frete 400 ms) não usam os tokens zerados. A medição "0 animações" foi feita só no carregamento, antes de adicionar item à sacola. `reduceMotion` em app.js:10 é lido uma vez (não reage a mudança). Origem: leitura. | Envolver `bump` e as transições literais em `@media (prefers-reduced-motion: reduce){ *{animation:none!important; transition:none!important} }` ou usar `var(--motion-*)`; ouvir `change` do matchMedia. Repetir a medição após adicionar item. |
| QA-03 | média | styles.css:314-316 | Névoa do hero anima em loop infinito (26/34/40 s) sem controle de pausa. WCAG 2.2.2 (A) exige mecanismo de pausa para movimento automático acima de 5 s, salvo essencial; hoje só quem ativou movimento reduzido fica livre. Interpretação que pede revisão humana (Quality Specialist). | Pausar após alguns segundos, oferecer botão de pausa, ou tornar a névoa estática. |
| QA-04 | média | app.js:278-282 | Corrida no rótulo do botão "Adicionar": `original` é lido do texto atual. Dois cliques em menos de 1,6 s (comum para levar 2 unidades) fazem o segundo timer restaurar "Adicionada à sacola" como se fosse o original; no desktop o botão fica com o texto errado e sem o estilo `is-done`. O timer 1 também desfaz o estado do clique 2 antes da hora. Origem: leitura, não reproduzido. | Guardar o rótulo original em `data-label` na carga e manter um timer por botão (`clearTimeout` antes de reagendar). |
| QA-05 | média | index.html:180 (e os outros 19 botões); styles.css:444-449 | Os 20 botões têm o mesmo nome ("Adicionar à sacola") sem o produto; leitor de tela navegando por botões não distingue as peças. No celular o texto real (`font-size:0`, ainda lido) soma-se ao `::after` ("Adicionar"), duplicando o nome. Origem: leitura. | `aria-label="Adicionar Caneca Névoa à sacola"` (mantém o texto visível "Adicionar" dentro do nome, WCAG 2.5.3) e trocar o truque `font-size:0` por dois spans (`.add__long`/`.add__short`) com `display`. |
| QA-06 | média | app.js:201-204; index.html:149-154 | Ao acionar "Limpar filtro", a barra fica `hidden` e o botão focado some; o foco cai no `body` (WCAG 2.4.3). Origem: leitura. | Mover o foco para o título de `#categorias` (como já se faz ao filtrar, app.js:198-199). |
| QA-07 | média | app.js:135-136; styles.css:407 | Seta "próximas peças" passa a `disabled` enquanto tem foco (ao alcançar a última página por teclado); o foco é perdido ou fica preso, com comportamento diferente por navegador. Origem: leitura; comportamento por navegador não testado. | Usar `aria-disabled="true"` e ignorar o clique, mantendo o botão focável; ou mover o foco para a seta oposta. |
| QA-08 | média | app.js:209, 273-275, 296 | `localStorage` não é validado: valor JSON que não seja array (ex.: `{}`) faz `cart.forEach`/`cart.filter` lançar erro e quebra a sacola até limpar o storage; `qty` não numérico gera "NaN"; preço, nome e imagem vêm do storage e não do catálogo (preço antigo persiste se o catálogo mudar; peça esgotada continua na sacola); sem limite de quantidade. Sem sincronia entre abas (última gravação vence). Cenário de risco baixo (chave própria, sem PII), mas é robustez básica. | Validar `Array.isArray` e cada item (id existente no DOM, `qty` inteiro 1..N); reidratar nome/preço/imagem a partir do botão `[data-add=id]`; opcional: evento `storage`. |
| QA-09 | média | index.html:26, 37, 43, 166, 180, 568-570; styles.css:158; app.js:3 | Sem JavaScript, abaixo de 1024 px **não existe navegação** (menu `.nav` oculto e gaveta com `hidden`); os botões "Adicionar", "Sacola" e "Finalizar compra" aparecem mas não fazem nada. O comentário em app.js:3 ("sem JS ... as âncoras funcionam") só vale para os links do corpo da página. Origem: leitura; não executado com JS desligado. | `<noscript>` com a lista de âncoras, ou classe `no-js` que exibe o `.nav` e esconde botões de compra; corrigir o comentário. |
| QA-10 | média | evidence/DEV-002/render/pagina-1440-full.png, pagina-375-full.png | As capturas de página inteira mostram cartões **sem ilustração** nas vitrines Terra Molhada e Sal (em 1440: 5 dos 8 cartões visíveis dessas duas vitrines sem imagem; em 375 também). O padrão (cartões alternados) sugere imagens `loading="lazy"` não carregadas no momento da captura, mas **não consigo afirmar** se é artefato de captura ou defeito. Esse material, como está, não comprova a aparência das coleções passadas. | Developer: recapturar rolando a página até cada vitrine ou aguardando `img.complete` em todas; anexar a nova evidência. QA reexecuta no reteste. |
| QA-11 | média | styles.css:389 | Bullet inativo usa `--stone-300` (#BDB7AC) sobre #F4F1EC: contraste estimado ~1,8:1, abaixo de 3:1 (WCAG 1.4.11, AA) para identificar o controle e o estado. O estado ativo se distingue pela largura, mas o controle inativo é quase invisível. Estimativa manual, não medida por script. | Usar `--ink-700` ou `--text-secondary` no ponto inativo; conferir com o script de contraste do UI-001. |
| QA-12 | baixa | app.js:66-75, 33-47 | Gavetas `aria-modal` sem `inert` no resto da página: se o foco estiver no `body` (ex.: clique em texto do painel), Tab escapa para a página por trás. | Aplicar `inert` em header/main/footer enquanto a gaveta estiver aberta. |
| QA-13 | baixa | styles.css:27, 360 | Com filtro ativo, a barra de filtro sticky (52 px) soma-se ao header (64/76 px), mas `scroll-padding-top` fica em 88 px: âncoras e foco por teclado ficam parcialmente cobertos. Não chega a ocultar por inteiro (2.4.11 provavelmente atendido), porém prejudica. | Definir `scroll-padding-top` maior quando `.filterbar` estiver visível. |
| QA-14 | baixa | index.html:64-65; app.js:176-178 | Com filtro ativo, links "Terra Molhada"/"Sal" do menu apontam para blocos `hidden` e não acontece nada, sem aviso. | Limpar o filtro ao navegar para âncora de coleção ou avisar. |
| QA-15 | baixa | index.html:167-168, 309-310, 404-405; app.js:119 | Três carrosséis com setas e bullets de mesmo nome ("Peças anteriores", "Página 1 de 4") e contêiner de bullets sem rótulo: o leitor não sabe a qual vitrine pertencem. | `role="group"` + `aria-label` por vitrine; incluir o nome da coleção nos rótulos. |
| QA-16 | baixa | index.html:302 vs 319 | Hierarquia de títulos: nome da coleção (h3) e nome de cada peça (h3) estão no mesmo nível. | Peças em h4 nas coleções passadas. |
| QA-17 | baixa | styles.css:27, 145, 327 | Estética (decidir com UI/Art Director): (a) header a 92% de opacidade deixa vazar a vitrine por trás (visível em `filtro-vasos-375.png`, textos "Travessas/Vasos e jarras" fantasmas); (b) ao saltar para `#novidades` sobram ~64 px de faixa vazia sob o header (visível em `vitrine-375.png`): padding da seção + `scroll-padding`. | Header ~97% ou opaco; `scroll-margin-top` compensando o padding da seção. |
| QA-18 | baixa | styles.css:29, 339 | `100vw` no cálculo dos cartões e categorias inclui a barra de rolagem clássica: em janela estreita de desktop o "30% do 3º cartão" passa de 30%. Não afeta celular real. | Usar `100%` do contêiner ou `container-type`. |
| QA-19 | baixa | styles.css:444-449 | Em 320 px o cartão tem ~122 px; "Adicionada" + ícone + padding tende a passar de 122 px (estimativa ~127 px) e vazar do botão no estado `is-done`. Não medido. | Reduzir padding/ícone em < 360 px ou rótulo "Ok". |
| QA-20 | baixa | styles.css:138-140, 445; index.html:50, 500, 505 | Conteúdo: (a) aviso "Loja demonstrativa" some abaixo de 600 px (só no rodapé e no aviso do checkout); (b) "sem juros" some abaixo de 768 px, deixando só "3x de R$ 32,67"; (c) FAQ fala em "fechar o pedido"/"fechamento do pedido", que não existe; (d) nav da gaveta rotulada "Menu do celular" também aparece em tablet. | Manter o aviso curto no celular; manter "sem juros"; ajustar textos; rotular "Menu principal". |
| QA-21 | baixa | tokens.css:1, 94; styles.css:25 | Cabeçalho de tokens.css ainda diz "PROPOSTA, NÃO APROVADA" (UI-001 foi aprovado); `--container` de 72rem é sobrescrito por 80rem em styles.css (documentação desatualizada). 10 SVGs gerados não são usados (nevoa-ramequim, nevoa-bojudo, terra-xicara, terra-travessa, terra-garrafa, terra-jarra, sal-caneca, sal-garrafa, sal-copo, sal-bojudo). | Atualizar comentário; remover ou documentar os assets não usados. |
| QA-22 | baixa | styles.css:67, 240-243, 268-275, 314-316; app.js:81 | Riscos não medidos: (a) `body.is-locked` com `overflow:hidden` remove a barra de rolagem clássica e desloca o layout ao abrir a sacola no desktop; (b) custo de desempenho em celular fraco (ruído SVG `feTurbulence` em tela cheia com `mix-blend-mode`, `blur`, `backdrop-filter`, três animações infinitas); (c) `matchMedia(...).addEventListener` falha em Safari < 14 e interromperia o script. | Medir em dispositivo/perfil lento; `scrollbar-gutter: stable`; fallback `addListener`. |

## 4. O que foi verificado (leitura/análise)

- Leitura integral: `site/index.html`, `site/styles.css`, `site/app.js`, `site/tokens.css`, `scripts/gerar_site.py`, `interaction-check.json`, `handoffs/DEV-002.md`, `handoffs/approval-log.md`; `scripts/gerar_pecas.py` lido só nas primeiras 120 linhas (de 284), suficiente para o catálogo de formas/esmaltes, não para a geração de SVG completa.
- Capturas vistas: `vitrine-375.png`, `menu-aberto-375.png`, `sacola-375.png`, `filtro-vasos-375.png`, `pagina-375-full.png`, `pagina-1440-full.png`, `vitrine-pagina2-1440.png`.
- Requisitos do pedido e AC-ECOM-01..07 cruzados com código e medições (seção 2).
- Lógica do carrossel conferida analiticamente para 320, 375, 768, 1024 e 1440 px: `perPage`, `step`, `pages` e `current()` reproduzem os valores medidos (4/4/3/2/2 bullets; 4 cartões no desktop); limites do último trilho (`max scroll`) tratados em `current()`.
- Filtro: visibilidade de `li`, blocos `.past`, `#novidades`, introdução e barra; contagens das categorias contra o catálogo (6+3+5+2+4 = 20); resultado "Vasos e jarras" = 4 peças confere.
- Sacola: soma, parcelas (arredondamento correto de 98/3, 92/3, 128/3, 196/3), frete grátis em exatamente R$ 299, remoção por quantidade 0, escape de HTML (textContent, sem XSS identificado por leitura), fallback quando `localStorage` falha.
- Gavetas: `aria-modal`, nome, foco inicial, armadilha de Tab, Esc, retorno de foco, fechamento por link e por scrim, fechamento do menu ao passar para ≥ 1024 px.
- HTML: sem IDs duplicados; todos os `aria-labelledby` e `aria-controls` resolvem; todos os 20 SVGs referenciados existem; `hidden` combinado com `display` tratado em todos os elementos relevantes (li, dots, nav, filterbar, cart); `<script defer>` executa depois do script inline de `BRUMA_FRETE_GRATIS`. Não rodei validador W3C.
- Contraste (estimativa manual dos pares usados): texto principal e secundário sobre fog, texto inverso sobre ink-900, botão primário (fog-50 sobre clay-700) e rótulos do hero sobre o gradiente parecem passar 4,5:1; exceção: bullet inativo (QA-11). Alvos de toque: 44 px nos botões principais, 28 px nos bullets e 36 px em quantidade/remover/chip (acima do mínimo de 24 px do WCAG 2.5.8).
- Conformidade dos conteúdos: sem contato/encomenda; sem dado pessoal, segredo ou serviço externo no código lido; `noindex` presente; nenhuma requisição a terceiros vista.

## 5. O que NÃO foi verificado

- Execução de qualquer tipo (inclusive reprodução das medições da outra sessão), JavaScript desligado, Firefox, WebKit/Safari real, Android real, teclado virtual, zoom de 200/400%, espaçamento de texto.
- axe-core, Lighthouse, métricas de desempenho (laboratório e campo; `NOT_MEASURED_FIELD`), peso real de SVGs e fontes.
- Leitor de tela (NVDA, VoiceOver, TalkBack): os achados de nome acessível vêm de leitura de código, não de áudio.
- Aparência em 768 e em 1024 px (só números do JSON, sem captura), sobreposição do hero em 1024, 320 px de largura.
- Fidelidade ao Figma/UI-002: não havia frame aprovado referenciado; avaliação estética delegada a UI/Art Director e Quality Specialist.
- Segurança além de leitura estática: sem SCA, sem secret scanning, sem cabeçalhos HTTP (sem servidor).
- Sincronia byte a byte entre `index.html` e a saída de `gerar_site.py` (conferi estrutura e conteúdo por leitura; não rodei o gerador nem diff).
- Aprovação formal de UX-002/UI-002: `handoffs/approval-log.md` registra só DNA, UX-001, UI-001 e a rejeição de DEV-001. `docs/ux/revisao-002-ecommerce.md` e `docs/ui/revisao-002.md` existem, mas não há registro de aprovação do proprietário; a regra do CLAUDE.md exige UX/UI aprovados antes do desenvolvimento.

## 6. Veredito: NO-GO (para a aprovação do QA gate do DEV-002)

Motivos:
1. QA-01 (alta): botão da sacola sem nome acessível no celular/tablet.
2. QA-02: AC-ECOM-06 não atendido pelo código (a medição de terceiros só cobriu o carregamento).
3. QA-10: a evidência visual das coleções passadas está incompleta.

Atribuição de confiança: **média**. Os requisitos de layout e comportamento do pedido do proprietário parecem atendidos, mas toda a conclusão vem de leitura e de medições de terceiros, sem execução independente.

Caminho curto para GO COM RESSALVAS (decisão do proprietário, QA não concede waiver): corrigir QA-01, QA-02, QA-04, QA-05, QA-06 e QA-07 (todas pequenas), recapturar as imagens (QA-10), e o proprietário aceitar formalmente por escrito os demais itens médios/baixos (QA-03, 08, 09, 11) como backlog. Reteste obrigatório dos itens corrigidos mais regressão de sacola e carrossel, com Playwright (teclado, duplo clique, `reducedMotion`, JS desligado) e axe nos estados com gaveta e filtro abertos.

Necessita revisão humana: estética do banner e "rigor estético" (proprietário/UI), QA-03 e acessibilidade qualitativa (Quality Specialist), Safari/iPhone real.

## 7. Bloco para o Orchestrator

```json
{
  "agent": "eixo-qa-engineer",
  "version": "1.0",
  "project_id": "eixo-piloto-01",
  "project_dna_version": "0.2.0",
  "commit": "UNAVAILABLE",
  "environment": "none",
  "verdict": "NO_GO",
  "tests": {"planned": 0, "implemented": 0, "executed": 0, "passed": 0, "failed": 0, "skipped": 0, "flaky": 0},
  "critical_journeys": {"total": 0, "passed": 0, "not_tested": 0},
  "coverage_scope": [
    "revisão estática de site/index.html, styles.css, app.js, tokens.css, scripts/gerar_site.py e parte de gerar_pecas.py",
    "leitura de interaction-check.json (medição de terceiros, não reproduzida) e de 7 capturas PNG"
  ],
  "not_tested": [
    "qualquer execução (Playwright, axe, Lighthouse)",
    "JS desligado, Firefox, WebKit, dispositivos reais, leitor de tela",
    "768/1024 px visualmente; desempenho; segurança além de leitura",
    "aprovação formal de UX-002/UI-002 (ausente em approval-log.md)"
  ],
  "findings": [
    {"id": "QA-01", "severity": "alta", "ref": "site/index.html:37-39; site/styles.css:165,194"},
    {"id": "QA-02", "severity": "media", "ref": "site/styles.css:174-175; AC-ECOM-06"},
    {"id": "QA-10", "severity": "media", "ref": "evidence/DEV-002/render/pagina-1440-full.png"},
    {"id": "QA-03..QA-09,QA-11", "severity": "media", "ref": "ver tabela em parecer-qa.md"},
    {"id": "QA-12..QA-22", "severity": "baixa", "ref": "ver tabela em parecer-qa.md"}
  ],
  "evidence": [
    "evidence/DEV-002/render/interaction-check.json",
    "evidence/DEV-002/render/vitrine-375.png",
    "evidence/DEV-002/render/pagina-1440-full.png",
    "evidence/DEV-002/qa/parecer-qa.md"
  ],
  "blockers": ["QA-01", "QA-02 (AC-ECOM-06)", "QA-10 (evidência visual incompleta)", "registro de aprovação UX-002/UI-002 ausente"],
  "accepted_risks": [],
  "recommendation": "Developer corrige QA-01, QA-02, QA-04..QA-07 e recaptura as imagens; QA reexecuta com Playwright + axe; proprietário decide sobre os itens médios/baixos restantes.",
  "needs_human_review": ["estética do banner/rigor estético (proprietário, UI/Art Director)", "QA-03 e acessibilidade qualitativa (Quality Specialist)", "Safari/iPhone real", "aprovação UX-002/UI-002"]
}
```
