# Revisão UX-002: de vitrine informativa a loja demonstrativa

**Projeto:** piloto-01 · **Data:** 2026-10-22 · **Origem:** feedback do proprietário sobre a PR #7 (DEV-001), que rejeitou o layout
**Autor:** sessão do projeto (Claude Code), sem delegação ao eixo-ux-architect nesta rodada; ver "Limites" no fim
**Substitui em `ux-spec.md`:** §1 (objetivo, CTA único, fora de escopo), §2 (jornada P0 e fluxos de contato), toda menção a encomenda e contato. O resto (princípios de prova por processo, tom, acessibilidade) continua valendo.

> Legenda: **[FATO]** pesquisa citada · **[HIPÓTESE]** · **[FICTÍCIO]** · **[DECISÃO]** (desta revisão, pedida pelo proprietário).

## 1. Novo enquadramento

| Item | Antes (UX-001) | Agora (UX-002) | Tipo |
|---|---|---|---|
| Objetivo | Levar à coleção e ao contato. Não vende. | Loja: descobrir peças, comparar preços e montar a sacola. Nenhuma compra é processada. | DECISÃO do proprietário |
| CTA principal | "Conhecer a coleção" | "Comprar a coleção" (banner) + "Adicionar à sacola" em cada peça | DECISÃO |
| Contato / encomenda | Seção Contato, prazo de encomenda 45 dias | Removidos por completo | DECISÃO do proprietário |
| Navegação no celular | Links soltos no header | Menu hambúrguer em gaveta lateral | DECISÃO do proprietário |
| Coleção | 6 cartões grandes empilhados | Vitrines em carrossel: atual (8) + 2 coleções passadas (6 cada) | DECISÃO do proprietário |
| Descoberta por tipo | Não havia | 5 categorias com filtro em todas as vitrines | DECISÃO do proprietário |

Público, barreiras e contexto de uso continuam os da pesquisa: mulheres de 25 a 44 anos, chegando pelo celular a partir de redes sociais, com barreiras de acabamento (39%) e preço (27%) **[FATO, Pesquisa §1.1]**. O carrossel com corte do terceiro cartão responde ao contexto de celular; o preço com parcelamento responde à barreira de preço **[HIPÓTESE]**.

## 2. Jornada P0 nova

| Passo | Objetivo do usuário | Elemento | Saída |
|---|---|---|---|
| 1. Chegada | Entender o que é e sentir a marca | Banner da Coleção Névoa | Lê "A névoa virou mesa." e vê as peças |
| 2. Escolher caminho | Ir direto às peças ou a um tipo | "Comprar a coleção" ou categorias | Chega à vitrine certa |
| 3. Explorar | Comparar peças | Carrossel: arrastar (celular) ou setas/bullets (desktop) | Encontra uma peça de interesse |
| 4. Confiar | Tirar dúvida de qualidade | Faixa "O ateliê" e Ajuda | Sabe que vai ao micro-ondas e à lava-louças |
| 5. Decidir | Guardar a peça | "Adicionar à sacola" | Contador da sacola sobe, aviso confirma |
| 6. Revisar | Ver total e frete | Gaveta da sacola: quantidade, subtotal, barra de frete grátis | Vê quanto falta para frete grátis |
| 7. Fim | Fechar o pedido | "Finalizar compra" | Aviso de loja demonstrativa (nenhum pedido é criado) |

Fluxos alternativos: categoria pelo menu do celular; link profundo para `#colecoes`, `#colecao-terra`, `#colecao-sal`, `#ajuda`; sem JavaScript as vitrines continuam rolando na horizontal e as âncoras funcionam, mas sacola e filtro não (aceito para um protótipo demonstrativo).

## 3. Arquitetura da home

1. Faixa de aviso (frete grátis; loja demonstrativa no desktop)
2. Header fixo: hambúrguer (< 1024 px) · logo · menu (≥ 1024 px) · sacola com contador
3. Banner artístico
3a. Vantagens: frete, troca, embalagem, pagamento (logo abaixo do banner, pedido do proprietário em 2026-10-22)
4. Categorias (5)
5. Novidades da fornada: Coleção Névoa, carrossel
6. O ateliê: faixa escura com 3 fatos de material
7. Coleções passadas: Terra Molhada e Sal, cada uma com seu carrossel
8. (movido) Vantagens: ver item 3a
9. Ajuda: envio, trocas, cuidados, pagamento (acordeão)
10. Rodapé de loja

## 4. Regras do carrossel

| Aspecto | Desktop ≥ 1024 px | Tablet 768–1023 px | Celular < 768 px |
|---|---|---|---|
| Cartões visíveis | 4 inteiros | 3 + corte do 4º | 2 + cerca de 30% do 3º |
| Navegação | Setas (avançam uma página) + bullets clicáveis | Arrastar + bullets | Arrastar + bullets |
| Margem | Dentro do container | Trilho sangra até a borda direita | Idem |
| Estados | Seta anterior desabilitada na 1ª página, próxima na última | - | - |

Por que diferente: no desktop o cursor precisa de um alvo explícito e as setas comunicam navegação; no celular o corte proposital do cartão seguinte já ensina o gesto de arrastar, e as setas competiriam com o polegar. Os bullets, nos dois, mostram quantas páginas existem **[DECISÃO do proprietário]**.

## 5. Conteúdo fictício novo

| Dado | Valor | Base |
|---|---|---|
| Coleções | Névoa (primavera 2026, atual), Terra Molhada (outono 2026), Sal (verão 2025/26) | FICTÍCIO |
| Peças e preços | R$ 58 (ramequim) a R$ 210 (travessa) | Faixa dos ateliês da Pesquisa §1.2 (Ise, AMME, Cafaz) e preços já aprovados na UX-001 |
| Frete grátis | acima de R$ 299 | FICTÍCIO, perto de 3 peças médias |
| Parcelamento | 3x sem juros a partir de R$ 90 | FICTÍCIO, prática comum no varejo online |
| Troca | 7 dias | Direito de arrependimento do CDC (art. 49) para compras fora do estabelecimento |
| Esgotados | 2 peças de coleções passadas | FICTÍCIO, mostra o estado "Esgotado" |

Proibições mantidas: sem depoimentos, avaliações, selos ou urgência inventados; sem dados pessoais; sem checkout, pagamento ou integração real.

## 6. Critérios de aceite novos (verificados em `evidence/DEV-002/render/interaction-check.json`)

- AC-ECOM-01: abaixo de 1024 px o menu é um botão "Abrir menu"; a gaveta abre, prende o foco, fecha com Esc, X ou toque fora, e devolve o foco ao botão.
- AC-ECOM-02: nenhuma rolagem horizontal da página em 320, 375, 768, 1024 e 1440 px.
- AC-ECOM-03: carrossel mostra 4 cartões no desktop com setas e bullets; 2 + corte do 3º no celular, sem setas, com bullets.
- AC-ECOM-04: "Adicionar à sacola" atualiza o contador e o subtotal; quantidade e remover funcionam; "Finalizar compra" mostra o aviso de loja demonstrativa.
- AC-ECOM-05: categoria filtra todas as vitrines e mostra a barra "Mostrando: X" com "Limpar filtro".
- AC-ECOM-06: com `prefers-reduced-motion: reduce`, nenhuma animação roda.
- AC-ECOM-07: a página não contém seção de contato nem menção a encomenda.

## Limites

Esta revisão foi escrita diretamente pela sessão do projeto, a partir do feedback do proprietário, para não atrasar a entrega; o eixo-ux-architect não foi acionado. A revisão independente do resultado foi delegada ao eixo-qa-engineer (`evidence/DEV-002/qa/`). Não houve teste com pessoas.
