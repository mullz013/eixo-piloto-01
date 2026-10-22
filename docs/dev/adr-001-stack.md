# ADR-001: Stack da landing page Ateliê Bruma

**Projeto:** piloto-01 · **Task:** DEV-001 · **DNA:** v0.2.0 (briefing fictício) · **Status:** proposta do Developer, dentro da restrição do briefing da tarefa (HTML + CSS puros). **Não é release.**

## Contexto
Uma página única, estática, com 5 seções, um CTA de âncora, sem formulário, sem coleta de dados, sem venda, sem analytics. UX exige que tudo funcione sem JavaScript (AC-NAV-05) e a UI proíbe recursos externos. Deploy está proibido neste piloto.

## Opções
| Opção | Prós | Contras |
|---|---|---|
| A. HTML + CSS puros, sem build | Menor superfície de erro e de segurança; zero dependências; auditável a olho; funciona sem JS por construção | Marcação repetida nos 6 cartões; sem minificação |
| B. Gerador estático (Astro, Eleventy) | Componentes, minificação | Dependências e build sem necessidade; contraria a restrição |
| C. Next.js / React | Ecossistema | Bundle JS, SSR/SSG e tooling para uma página sem estado; viola AC-NAV-05 como padrão |

## Decisão
**Opção A.** Arquivos em `site/`: `index.html`, `styles.css`, `tokens.css` (cópia de `docs/ui/tokens.css`, valores inalterados), `assets/` (SVGs do logotipo e favicon) e `fonts/` (WOFF2 auto-hospedadas, preparadas fora desta tarefa).

Escolhas relevantes:
- Rolagem suave, estados e layout em CSS; `scroll-behavior: smooth` só sob `prefers-reduced-motion: no-preference`.
- Âncoras nativas (`#colecao` etc.), `scroll-padding-top` e `scroll-margin-top` de 5rem para o header fixo.
- Logotipo como `<img>` de SVG (alt "Ateliê Bruma"), não SVG inline, para manter o estado "imagem falhou" previsto na UI.
- Placeholders de imagem em CSS puro (`div role="img"` com `aria-label` do alt aprovado), sem arquivos de imagem e sem licenças pendentes.
- `font-display: swap` e fontes de fallback com `size-adjust` (valores estimados).
- `color-mix()` apenas para o gradiente decorativo e o hover do rodapé, com declaração anterior de fallback no gradiente.

## Custo, risco e reversibilidade
- Custo de infra e de operação: nulo (arquivos estáticos). Custo de IA: nenhum.
- Risco: duplicação de marcação dos cartões; mudança de copy exige edição manual (qualquer mudança de copy volta ao UX, de qualquer forma).
- Reversível: migrar para um gerador estático depois é trivial porque não há lógica.

## Fora de escopo e não feito
Nenhum deploy, domínio, headers HTTP, CSP ou cache foi configurado. Se a página for publicada um dia, abrir ADR própria (hospedagem, `Content-Security-Policy` restritiva, cabeçalhos de cache das fontes, `robots`/`noindex` em nível de servidor).

## Decisão aprovada
Pendente de aprovação humana (esta ADR registra a escolha do Developer sob a restrição do briefing).
