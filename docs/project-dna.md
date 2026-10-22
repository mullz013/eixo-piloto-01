# Project DNA — EIXO Piloto 01

**Estado:** APPROVED · **Versão:** 0.2.0 · **Perfil:** LITE.

> O proprietário autorizou em conversa o uso de **Ateliê Bruma**, marca **100% fictícia**, como piloto de avaliação da esteira EIXO. Esta aprovação **não autoriza** publicar, contratar serviços, utilizar dados reais ou considerar UX/UI aprovados.

## 1. Instruções e objetivos
- **Cliente fictício:** Ateliê Bruma, ateliê de cerâmica autoral.
- **Objetivo:** testar delegações reais e handoffs entre os seis agentes para uma loja demonstrativa (e-commerce sem checkout real). *Emenda de 2026-10-22, ver abaixo.*
- **Público (hipótese):** interessados em design, cerâmica autoral e peças artesanais para casa.
- **Jornada P0:** entender a proposta → explorar vitrines e categorias → adicionar à sacola → revisar a sacola (finalizar mostra aviso de loja demonstrativa).
- **CTA:** “Comprar a coleção” (âncora para a vitrine) e “Adicionar à sacola” em cada peça.
- **Fora do escopo:** dados reais, checkout, pedidos e pagamentos reais, encomendas e contato para encomendar, domínio, deploy, WhatsApp.

## 2. Contexto do projeto
- UX Architect deve propor jornadas, arquitetura, conteúdo demonstrativo e critérios mensuráveis.
- UI Designer & Art Director deve criar direção de arte **exclusiva para a marca**, tipografia, tokens, estados e responsividade; **não usar a identidade corporativa da EIXO**.
- Assets e imagens ainda requerem definição/licenciamento; não inventar depoimentos ou avaliações reais.
- **Nenhum arquivo Figma, arte, token ou layout foi aprovado**. Aprovação de briefing não é aprovação de UI.

## 3. Ferramentas e validação
- **GitHub privado:** `mullz013/eixo-piloto-01`.
- **Agentes versionados:** `mullz013/eixo-ai` (instalar no Claude Code antes do ensaio).
- **Stack:** proposta pelo Developer só após critérios UX/UI.
- **Validações:** semântica, responsividade, acessibilidade, SEO, testes reais e evidência de delegação.
- **Deploy:** bloqueado, exigindo autorização específica e gates independentes.

## Emenda de escopo (2026-10-22)
Na revisão da PR #7 o proprietário rejeitou o layout e pediu: “Quero que você torne isso como se fosse um e-commerce mesmo [...] para que não tenha contatos para a pessoa encomendar”. O escopo passa de landing page informativa para loja demonstrativa. Marca, público e restrições de dados não mudam, por isso a versão continua 0.2.0. Detalhes em `docs/ux/revisao-002-ecommerce.md`.

## Registros de aprovação
| Versão | Decisão | Responsável | Origem |
|---|---|---|---|
| 0.1.0 | DRAFT | — | Abertura técnica |
| 0.2.0 | **APPROVED apenas para briefing e teste controlado** | Proprietário da EIXO | Confirmação em conversa: “Beleza, mete o bronco aí.” |

## O que **ainda não aconteceu**
- Nenhum agente Claude Code foi invocado e não há handoff especializado realizado.
- UX/UI não foram produzidos nem aprovados; nenhum site foi desenvolvido ou publicado.
- Inicialização automática de novo repositório pelo Orchestrator continua por testar.
