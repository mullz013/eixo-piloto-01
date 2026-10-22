# Aprovações do piloto

## DNA — v0.2.0
- Decisão: **APROVADO para marca fictícia Ateliê Bruma e experimentos de colaboração dos agentes**.
- Origem: conversa com o proprietário, resposta “Beleza, mete o bronco aí.” à proposta do piloto.
- Registro: 2026-10-21.
- Não cobre: aprovação de layouts, implementação definitiva, contratação de serviços, publicação ou criação de credenciais.
- Observação: declaração capturada no chat, não é evidência de execução de agentes em runtime.

## UX-001 — Ateliê Bruma
- Decisão: **APROVADO** (arquitetura, jornada P0, conteúdo demonstrativo, critérios de aceite e handoff para UI em `docs/ux/`).
- Origem: conversa do projeto, 2026-10-22T00:27:51Z. O proprietário escolheu revisar antes, revisou a PR #5 (commit e1d8da8) e respondeu "Tudo certo".
- Decisões incorporadas antes: logotipo a ser proposto pela UI, CTA direto para `#colecao`, dica de temperatura mantida, endereço fictício "Rua da Bruma Clara, 214, Curitiba (PR)".
- Não cobre: logotipo, paleta, tipografia, layouts finais, implementação, publicação ou contratação de serviços.

## UI-001 — Ateliê Bruma
- Decisão: **APROVADO** (direção de arte "Névoa quieta", logotipo, tokens e handoff para o Developer em `docs/ui/`).
- Origem: conversa do projeto, 2026-10-22T10:23:04Z. O proprietário revisou a PR #6 (commit 4cd5343) e respondeu "Sim para as 3 perguntas" às perguntas: aprova direção e logotipo; mantém as faixas de bruma no símbolo; aceita o tracejado como marca de "fictício".
- Não cobre: implementação, fotos reais, publicação ou contratação de serviços.

## DEV-001 — Ateliê Bruma
- Decisão: **REJEITADO** (layout da PR #7).
- Origem: conversa do projeto, 2026-10-22T11:34:17Z. O proprietário apontou: retângulo vertical arredondado no topo (placeholder em arco), menu solto no celular, vitrine grande demais, ausência de categorias e coleções passadas, modelo de encomenda em vez de e-commerce, banner pouco artístico e falta de rigor estético.
- Consequência: emenda de escopo no DNA (loja demonstrativa) e DEV-002 em `handoffs/DEV-002.md`.

## DEV-002, UI-003, UI-004, DES-001, QA-001 e QUAL-001 — Ateliê Bruma
- Decisão: **APROVADO** (loja demonstrativa com layout UI-003/UI-004, fotos DES-001, revisões QA e Quality) e **merge autorizado** das PRs #8 e #9 deste repositório e da PR #3 de `mullz013/eixo-ai`.
- Origem: thread do projeto, 2026-10-22T17:19:12Z. O proprietário respondeu "Tudo aprovado, pode mergear" depois de receber o reteste no commit `afbd689`: QA PASS/GO (83 PASS, 0 FAIL, 2 P3 conhecidos) e Quality PASS_WITH_NOTES (P2 corrigidos).
- P3 aceitos para depois: CTA abaixo da dobra em 320×568 e 360×640; demais P3 em `evidence/QUAL-001/report.md`.
- Não cobre: deploy, domínio, hospedagem ou contratação de serviços (ORCH-RELEASE segue PENDING).

## PREVIEW-001 — prévia no GitHub Pages
- Decisão: **AUTORIZADO** publicar uma prévia do site (`site/`) no GitHub Pages para o proprietário navegar pelo celular.
- Origem: thread do projeto, 2026-10-22T17:53:12Z. O proprietário escreveu "sobre o site piloto, pode simular com esse GitHub Pages, só pra gente ver como é que tá".
- Forma: workflow `.github/workflows/pages-preview.yml`, só a pasta `site/`, página com `noindex`. Dados da loja seguem fictícios.
- Não cobre: release oficial (ORCH-RELEASE segue PENDING e `live_deploy_authorized` segue falso), domínio próprio, hospedagem paga ou contratação de serviços.
