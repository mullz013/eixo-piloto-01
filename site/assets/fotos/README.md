# Fotos do Ateliê Bruma (DES-001)

**Origem:** imagens **geradas por IA** no ChatGPT, manualmente, pelo proprietário (Matheus Santos) em 2026-10-22, a partir dos prompts escritos pelo papel `eixo-graphic-designer` (página de prompts: https://claude.ai/artifact/Xcr4KNxiW1B2dAnZEQQJZs). Não são fotografias de produto real nem imagens de banco; a marca é fictícia.

**Originais:** PNG 1024×1536, 1536×1024 e 1254×1254, guardados fora do repositório (Drive do proprietário, pasta `assets/fotos`).

**Derivados:** gerados por `python3 scripts/processar_fotos.py <pasta_dos_originais>` (Pillow, offline). WebP qualidade 80 em duas larguras para `srcset` + um JPG de fallback na maior largura.

| Pasta | Onde entra | Recorte | Larguras |
|---|---|---|---|
| `produtos/` | cartões das vitrines, sacola, cartão "Destaque da fornada" | 4:5 | 480, 800 |
| `categorias/` | "Compre por categoria" | 1:1 | 400, 640 |
| `banner/` | banner principal (desktop 3:2 com `object-fit`, celular 1:1) | | 1024/1536, 640/960 |
| `colecoes/` | sem uso no momento (a seção "Escolha sua coleção" foi removida a pedido do proprietário); mantidas para reuso | 3:2 | 800, 1536 |
| `atelie/` | painel "O ateliê" (`torno`); `fornada` fica como alternativa, não usada | 4:5 / 3:2 | 640, 1024 |
| `og/` | prévia de link (Open Graph), ainda sem `<meta>` porque precisa de URL absoluta | 1200×630 | |

As ilustrações SVG de `assets/pecas/` (scripts/gerar_pecas.py) deixaram de ser usadas pela página e ficam como histórico.
