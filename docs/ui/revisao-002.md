# Revisão UI-002: direção de arte da loja

**Projeto:** piloto-01 · **Data:** 2026-10-22 · **Origem:** feedback do proprietário sobre a PR #7
**Autor:** sessão do projeto (Claude Code), sem delegação ao eixo-ui-art-director nesta rodada
**Mantém de UI-001:** direção "Névoa quieta", logotipo, paleta, Fraunces + Figtree, tokens (`tokens.css` sem alteração de valor).
**Substitui de UI-001:** placeholder em arco no hero, motivo do traço tracejado como marca de "fictício", etiquetas "(exemplo)" por linha, composição de landing page.

## 1. O que muda e por quê

| Antes | Problema apontado | Agora |
|---|---|---|
| Placeholder em arco (999px no topo) no hero, tracejado | "Retângulo vertical arredondado em cima" vazio dominando a primeira dobra | Banner com natureza-morta ilustrada, sol de argila, névoa em movimento e palavra "névoa" em contorno |
| Tracejado = fictício, etiquetas "(exemplo)" | Página parecia rascunho, não loja | Aviso único e discreto: faixa do topo (desktop) e rodapé. Tracejado fica só no botão "Esgotado" |
| Cartões grandes de 1 coluna | "Vitrine gigantesca" | Cartões 4:5 em carrossel, 4 por vez no desktop |
| Sem imagem de produto | Qualidade dependia só de tipografia | Ilustrações SVG das peças, uma por forma e esmalte |

## 2. Sistema visual da loja

- **Grade:** container de 80rem (1280 px), gutter `clamp(1rem, 5vw, 2rem)`; gap dos cartões 12 / 16 / 24 px (celular / tablet / desktop).
- **Ritmo:** `--section-y` de UI-001 (64 px celular, 112 px desktop); categorias usam metade embaixo para colar na vitrine.
- **Títulos de seção:** Fraunces 300, `opsz` 96, tracking -0,015em. Rótulos ("kicker"): Figtree 600, 13 px, caixa-alta, tracking 0,14em.
- **Preço:** Fraunces 400, 22 px, algarismos alinhados; parcelamento em Figtree 13 px secundário.
- **Cartão de produto:** sem moldura; imagem 4:5 com raio 10 px sobre fundo da coleção (parede + mesa a 79%); nome 14 px 600; medida 13 px; botão contornado em pílula que inverte para tinta no hover e fica argila ao confirmar.
- **Cores por coleção (decorativas, sem texto por cima):** Névoa `#E6E7E3`/`#D6D8D3`, Terra Molhada `#EDE3D7`/`#DFCFBD`, Sal `#E1E7E8`/`#CDD6D8`. Texto continua em `--text-primary`/`--text-secondary` sobre `--background-canvas`, pares já aprovados em UI-001.
- **Argila (`#8A3F22`) só para ação:** botão principal, contador da sacola, barra de frete, ícones de vantagens.
- **Faixa escura** (`--background-inverse`) em dois pontos de respiro: "O ateliê" e rodapé.
- **Movimento:** entrada do banner em até 1,6 s, névoa em deriva lenta (26 a 40 s), zoom de 4,5% na imagem do cartão no hover. Tudo desligado com `prefers-reduced-motion`.

## 3. Banner

Composição em camadas, da trás para a frente: gradiente de névoa (creme para cinza-azulado) → sol de argila → palavra "névoa" em contorno a 22% de opacidade → mesa → peças (garrafa, jarra, tigela, xícara) com entrada escalonada → três faixas de névoa desfocadas em deriva → grão de papel em `multiply`. No desktop o texto ocupa a esquerda e a cena a direita, com a mesa atravessando a largura toda; no celular a cena vem primeiro (até 460 px) e o texto embaixo, com botão em largura total.

## 4. Ilustrações das peças

Geradas por `scripts/gerar_pecas.py`: cada forma é um sólido de revolução descrito por um perfil (altura, raio) em perspectiva leve. Camadas: corpo com degradê de 7 paradas, camada de esmalte com escorridos (névoa clara na Névoa, areia na Terra Molhada, borda cobalto no Sal), pé de argila crua, textura de grés (pintas por `feTurbulence`), sombra de contato e brilho especular. 10 formas × 3 esmaltes = 30 arquivos, 4 a 6 KB cada.

São ilustrações, não fotos. Para fotos de produto realistas, ver a recomendação do agente de design gráfico no documento de resolução do feedback.

## Limites

Escrita pela sessão do projeto, sem o eixo-ui-art-director. Contraste dos pares de texto não mudou em relação à UI-001 (mesmos tokens); os fundos novos de coleção não recebem texto. Avaliação visual feita pela sessão sobre capturas em 375 e 1440 px; não houve teste com pessoas.
