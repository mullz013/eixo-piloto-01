#!/usr/bin/env python3
"""Gera site/index.html da loja demonstrativa do Ateliê Bruma (marca fictícia).

O catálogo (CATALOGO) é a única fonte dos produtos: cada vitrine, a faixa de
categorias e os dados da sacola saem daqui. Estilo em site/styles.css,
comportamento em site/app.js. Ilustrações em scripts/gerar_pecas.py.

Uso: python3 scripts/gerar_site.py
"""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLECOES = [
    {
        "id": "nevoa", "nome": "Névoa", "estacao": "Primavera 2026", "atual": True,
        "frase": "Esmalte fosco cinza-azulado, com uma névoa clara que escorre da borda. A fornada da estação.",
    },
    {
        "id": "terra", "nome": "Terra Molhada", "estacao": "Outono 2026", "atual": False,
        "frase": "Óxido de ferro sobre argila escura: ferrugem embaixo, areia molhada em cima.",
    },
    {
        "id": "sal", "nome": "Sal", "estacao": "Verão 2025/26", "atual": False,
        "frase": "Branco quente de sal grosso, com a borda mergulhada em azul cobalto.",
    },
]

CATEGORIAS = [
    {"id": "canecas", "nome": "Canecas e xícaras", "formas": ["caneca", "xicara", "copo"], "arte": "nevoa-caneca"},
    {"id": "pratos", "nome": "Pratos", "formas": ["prato"], "arte": "sal-prato"},
    {"id": "tigelas", "nome": "Tigelas", "formas": ["tigela", "ramequim"], "arte": "terra-tigela"},
    {"id": "travessas", "nome": "Travessas", "formas": ["travessa"], "arte": "nevoa-travessa"},
    {"id": "vasos", "nome": "Vasos e jarras", "formas": ["garrafa", "bojudo", "jarra"], "arte": "terra-bojudo"},
]

# (colecao, forma, nome, medida, preco, selo)  selo: "novo" | "esgotado" | ""
CATALOGO = [
    ("nevoa", "caneca", "Caneca Névoa", "300 ml", 98, "novo"),
    ("nevoa", "xicara", "Xícara com pires Névoa", "120 ml", 84, "novo"),
    ("nevoa", "tigela", "Tigela funda Névoa", "Ø 15 cm · 600 ml", 92, ""),
    ("nevoa", "prato", "Prato raso Névoa", "Ø 26 cm", 128, ""),
    ("nevoa", "jarra", "Jarra Névoa", "1 litro", 168, "novo"),
    ("nevoa", "garrafa", "Vaso garrafa Névoa", "altura 22 cm", 186, ""),
    ("nevoa", "travessa", "Travessa oval Névoa", "32 × 22 cm", 210, ""),
    ("nevoa", "copo", "Copo Névoa", "250 ml", 72, ""),
    ("terra", "caneca", "Caneca Terra Molhada", "300 ml", 98, ""),
    ("terra", "bojudo", "Vaso bojudo Terra Molhada", "altura 18 cm", 196, ""),
    ("terra", "tigela", "Tigela funda Terra Molhada", "Ø 15 cm · 600 ml", 92, ""),
    ("terra", "prato", "Prato raso Terra Molhada", "Ø 26 cm", 128, "esgotado"),
    ("terra", "ramequim", "Ramequim Terra Molhada", "Ø 9 cm · 150 ml", 58, ""),
    ("terra", "copo", "Copo Terra Molhada", "250 ml", 72, ""),
    ("sal", "xicara", "Xícara com pires Sal", "120 ml", 84, ""),
    ("sal", "tigela", "Tigela funda Sal", "Ø 15 cm · 600 ml", 92, ""),
    ("sal", "jarra", "Jarra Sal", "1 litro", 168, ""),
    ("sal", "prato", "Prato raso Sal", "Ø 26 cm", 128, ""),
    ("sal", "travessa", "Travessa oval Sal", "32 × 22 cm", 210, "esgotado"),
    ("sal", "ramequim", "Ramequim Sal", "Ø 9 cm · 150 ml", 58, ""),
]

# momentos de uso (menu "Por momento"); uma peça pode estar em mais de um
MOMENTOS = [
    {"id": "cafe", "nome": "Café da manhã", "formas": ["caneca", "xicara", "copo", "tigela"]},
    {"id": "mesa", "nome": "Mesa posta", "formas": ["prato", "tigela", "copo", "ramequim"]},
    {"id": "servir", "nome": "Para servir", "formas": ["travessa", "jarra", "ramequim"]},
    {"id": "presentear", "nome": "Para presentear", "formas": ["caneca", "xicara", "garrafa", "bojudo"]},
]

PROXIMA_FORNADA = "14 de novembro"  # fictício

FRETE_GRATIS = 299

ICON = {
    "menu": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.5h18M3 12h18M3 17.5h12"/></svg>',
    "close": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.5 5.5l13 13M18.5 5.5l-13 13"/></svg>',
    "bag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 8.5h14l-1 12H6z"/><path d="M8.75 8.5V7a3.25 3.25 0 0 1 6.5 0v1.5"/></svg>',
    "prev": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.5 5.5L8 12l6.5 6.5"/></svg>',
    "next": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.5 5.5L16 12l-6.5 6.5"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13.5 6.5L19 12l-5.5 5.5"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 6.5h11v10h-11zM13.5 10h4l3 3.2v3.3h-7"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>',
    "swap": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8.5h14l-3.5-3.5M20 15.5H6l3.5 3.5"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13"/><path d="M12 7c-1.5-3-5-3.2-5-1.2S10 7 12 7zm0 0c1.5-3 5-3.2 5-1.2S14 7 12 7z"/></svg>',
    "card": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 6h19v12h-19zM2.5 10h19M6 14.5h4"/></svg>',
    "plus": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
}


FOTOS = "assets/fotos"


def foto(base: str, larguras: list[int], w: int, h: int, sizes: str, alt: str = "", cls: str = "",
         loading: str = "lazy", extra: str = "") -> str:
    """<picture> com WebP em srcset e JPG de fallback (gerados por scripts/processar_fotos.py)."""
    srcset = ", ".join(f"{FOTOS}/{base}-{lw}.webp {lw}w" for lw in larguras)
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img{c} src="{FOTOS}/{base}-{larguras[-1]}.jpg" width="{w}" height="{h}" alt="{escape(alt)}" '
            f'loading="{loading}" decoding="async"{extra}></picture>')


def brl(v: float) -> str:
    inteiro, cent = f"{v:.2f}".split(".")
    inteiro = f"{int(inteiro):,}".replace(",", ".")
    return f"R$ {inteiro}" if cent == "00" else f"R$ {inteiro},{cent}"


def categoria_de(forma: str) -> str:
    return next(c["id"] for c in CATEGORIAS if forma in c["formas"])


def filtros_de(forma: str) -> str:
    return " ".join([categoria_de(forma)] + [m["id"] for m in MOMENTOS if forma in m["formas"]])


def card(p: tuple, idx: int, hn: str = "h3") -> str:
    col, forma, nome, medida, preco, selo = p
    pid = f"{col}-{forma}"
    esgotado = selo == "esgotado"
    badge = ""
    if selo == "novo":
        badge = '<span class="badge">Novo</span>'
    elif esgotado:
        badge = '<span class="badge badge--muted">Esgotado</span>'
    parcela = ""
    if preco >= 90:
        parcela = f'<span class="price__inst">3x de {brl(preco / 3)}<span class="price__nojuros"> sem juros</span></span>'
    if esgotado:
        btn = f'<button class="add" type="button" disabled aria-label="Esgotado: {escape(nome)}">Esgotado</button>'
    else:
        btn = (
            f'<button class="add" type="button" data-add="{pid}" data-name="{escape(nome)}" aria-label="Adicionar à sacola: {escape(nome)}" '
            f'data-price="{preco}" data-img="{FOTOS}/produtos/{pid}-480.webp" data-col="{col}">'
            f'{ICON["plus"]}<span class="add__label"><span class="add__long">Adicionar à sacola</span><span class="add__short">Adicionar</span></span>'
            f'</button>'
        )
    return f'''          <li class="card card--{col}" data-cat="{filtros_de(forma)}">
            <div class="card__media">
              {foto(f"produtos/{pid}", [480, 800], 800, 1000, "(min-width: 1024px) 300px, 45vw", loading="eager" if idx < 4 and col == "nevoa" else "lazy")}
              {badge}
            </div>
            <div class="card__body">
              <{hn} class="card__name">{escape(nome)}</{hn}>
              <p class="card__meta">{escape(medida)} · grés</p>
              <p class="price"><span class="price__val">{brl(preco)}</span>{parcela}</p>
              {btn}
            </div>
          </li>'''


def vitrine(col: dict, titulo_id: str) -> str:
    itens = [p for p in CATALOGO if p[0] == col["id"]]
    hn = "h3" if col["atual"] else "h4"
    cards = "\n".join(card(p, i, hn) for i, p in enumerate(itens))
    return f'''      <div class="carousel" data-carousel data-name="{col["nome"]}">
        <div class="carousel__nav" hidden>
          <button class="arrow" type="button" data-dir="-1" aria-label="Peças anteriores de {col["nome"]}">{ICON["prev"]}</button>
          <button class="arrow" type="button" data-dir="1" aria-label="Próximas peças de {col["nome"]}">{ICON["next"]}</button>
        </div>
        <ul class="carousel__track" role="list" tabindex="0" aria-labelledby="{titulo_id}">
{cards}
        </ul>
        <div class="carousel__dots" role="group" aria-label="Páginas da vitrine {col["nome"]}" hidden></div>
      </div>'''


def secao_atual() -> str:
    col = COLECOES[0]
    return f'''  <section id="novidades" class="sec" aria-labelledby="t-novidades">
    <div class="wrap">
      <header class="sec__head">
        <div>
          <p class="tag tag--secondary">Coleção {col["nome"]} · {col["estacao"]}</p>
          <h2 id="t-novidades" class="sec__title">Novidades da <em>fornada</em></h2>
        </div>
        <p class="sec__aside">{col["frase"]}</p>
      </header>
{vitrine(col, "t-novidades")}
    </div>
  </section>'''


def secao_passadas() -> str:
    blocos = []
    for col in COLECOES[1:]:
        tid = f"t-col-{col['id']}"
        blocos.append(f'''    <div class="past past--{col["id"]}" id="colecao-{col["id"]}">
      <div class="wrap">
        <header class="sec__head sec__head--past">
          <div class="past__id">
            <p class="tag tag--secondary">{col["estacao"]}</p>
            <h3 id="{tid}" class="past__title">{col["nome"]}</h3>
          </div>
          <p class="sec__aside">{col["frase"]}</p>
        </header>
{vitrine(col, tid)}
      </div>
    </div>''')
    return f'''  <section id="colecoes" class="sec sec--past" aria-labelledby="t-colecoes">
    <div class="wrap">
      <header class="sec__intro">
        <h2 id="t-colecoes" class="sec__title">Coleções <em>passadas</em></h2>
        <p class="sec__lead">Fornadas anteriores que ainda têm peças no ateliê. Cada coleção tem um esmalte só dela.</p>
      </header>
    </div>
{chr(10).join(blocos)}
  </section>'''


def secao_categorias() -> str:
    tiles = []
    for c in CATEGORIAS:
        n = sum(1 for p in CATALOGO if p[1] in c["formas"])
        tiles.append(f'''        <li>
          <a class="cat cat--{c["id"]}" href="#novidades" data-filter="{c["id"]}" data-label="{c["nome"]}">
            <span class="cat__media">{foto(f"categorias/{c['id']}", [400, 640], 640, 640, "(min-width: 768px) 210px, 38vw")}</span>
            <span class="cat__name">{c["nome"]}</span>
            <span class="cat__count">{n} peças</span>
          </a>
        </li>''')
    return f'''  <section id="categorias" class="sec sec--cats" aria-labelledby="t-categorias">
    <div class="wrap">
      <header class="sec__head">
        <h2 id="t-categorias" class="sec__title">Compre por <em>categoria</em></h2>
        <p class="sec__aside">Toque numa categoria para ver só essas peças em todas as coleções.</p>
      </header>
      <ul class="cats" role="list">
{chr(10).join(tiles)}
      </ul>
    </div>
  </section>'''


def page() -> str:
    nav_cats = "\n".join(
        f'            <li><a href="#novidades" data-filter="{c["id"]}" data-label="{c["nome"]}">{c["nome"]}</a></li>' for c in CATEGORIAS
    )
    nav_momentos = "\n".join(
        f'            <li><a href="#novidades" data-filter="{m["id"]}" data-label="{m["nome"]}">{m["nome"]}</a></li>' for m in MOMENTOS
    )
    return f'''<!doctype html>
<html lang="pt-BR" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ateliê Bruma | Loja de cerâmica de mesa feita à mão (marca fictícia)</title>
<meta name="description" content="Loja demonstrativa do Ateliê Bruma, marca fictícia de cerâmica de mesa em grés feita à mão. Coleção Névoa e coleções passadas. Nenhuma compra é processada.">
<meta name="robots" content="noindex">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#F4F1EC">
<link rel="icon" type="image/svg+xml" href="assets/icone.svg">
<link rel="preload" href="fonts/fraunces-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/figtree-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/fraunces-italic-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="styles.css">
<script>document.documentElement.classList.remove("no-js");</script>
<script src="app.js" defer></script>
</head>
<body id="topo">

<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<aside class="announce" aria-label="Avisos da loja"><p>Próxima fornada: {PROXIMA_FORNADA} <span class="announce__sep" aria-hidden="true">·</span> <span class="announce__ship">Frete grátis acima de {brl(FRETE_GRATIS)}</span> <span class="announce__sep announce__sep--2" aria-hidden="true">·</span> <span class="announce__demo">Loja demonstrativa<span class="announce__long">: nenhuma compra é processada</span></span></p></aside>

<header class="header" data-header>
  <div class="wrap header__in">
    <button class="icon-btn header__menu" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu" data-open-menu>{ICON["menu"]}</button>
    <a class="brand" href="#topo"><img src="assets/logo-principal.svg" width="101" height="40" alt="Ateliê Bruma, início"></a>
    <nav class="nav" aria-label="Principal">
      <ul role="list">
        <li><a href="#novidades">Novidades</a></li>
        <li><a href="#categorias">Categorias</a></li>
        <li><a href="#colecoes">Coleções passadas</a></li>
        <li><a href="#atelie">O ateliê</a></li>
        <li><a href="#ajuda">Ajuda</a></li>
      </ul>
    </nav>
    <button class="bag-btn" type="button" aria-controls="sacola" aria-expanded="false" data-open-cart>
      {ICON["bag"]}<span class="bag-btn__label" aria-hidden="true">Sacola</span><span class="bag-btn__count" data-cart-count aria-hidden="true">0</span><span class="sr-only" data-cart-count-sr>Sacola, 0 itens</span>
    </button>
  </div>
</header>

<div class="drawer drawer--left" id="menu" data-drawer hidden>
  <div class="drawer__scrim" data-close></div>
  <div class="drawer__panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer__head">
      <img src="assets/logo-principal.svg" width="81" height="32" alt="Ateliê Bruma">
      <button class="icon-btn" type="button" aria-label="Fechar menu" data-close>{ICON["close"]}</button>
    </div>
    <nav class="mnav" aria-label="Menu principal">
      <ul role="list" class="mnav__main">
        <li><a href="#novidades">Novidades</a></li>
        <li><span class="mnav__group" id="g-peca">Por peça</span>
          <ul role="list" class="mnav__sub" aria-labelledby="g-peca">
{nav_cats}
          </ul>
        </li>
        <li><span class="mnav__group" id="g-momento">Por momento</span>
          <ul role="list" class="mnav__sub" aria-labelledby="g-momento">
{nav_momentos}
          </ul>
        </li>
        <li><a href="#colecoes">Coleções passadas</a>
          <ul role="list" class="mnav__sub">
            <li><a href="#colecao-terra">Terra Molhada</a></li>
            <li><a href="#colecao-sal">Sal</a></li>
          </ul>
        </li>
        <li><a href="#atelie">O ateliê</a></li>
        <li><a href="#ajuda">Ajuda</a></li>
      </ul>
    </nav>
    <p class="drawer__foot">Frete grátis acima de {brl(FRETE_GRATIS)}. Troca em até 7 dias.</p>
  </div>
</div>

<main id="conteudo" tabindex="-1">

  <section class="hero" aria-labelledby="t-hero">
    <div class="hero__stage" aria-hidden="true">
      <picture class="hero__photo">
        <source type="image/webp" media="(min-width: 1024px)" srcset="{FOTOS}/banner/desktop-1024.webp 1024w, {FOTOS}/banner/desktop-1536.webp 1536w" sizes="100vw">
        <source type="image/webp" srcset="{FOTOS}/banner/celular-640.webp 640w, {FOTOS}/banner/celular-960.webp 960w" sizes="100vw">
        <img src="{FOTOS}/banner/celular-960.jpg" width="960" height="960" alt="" fetchpriority="high" decoding="async">
      </picture>
      <div class="hero__mist hero__mist--1"></div>
      <div class="hero__mist hero__mist--2"></div>
      <div class="hero__mist hero__mist--3"></div>
    </div>
    <div class="hero__copy">
      <p class="tag tag--outline">Coleção Névoa<span class="tag__extra"> · Primavera 2026</span></p>
      <h1 id="t-hero" class="hero__title">A névoa<br> virou <em>mesa.</em></h1>
      <p class="hero__lead">Grés de alta temperatura, esmalte fosco e uma fornada por mês. Peças feitas à mão para usar todo dia.</p>
      <div class="hero__cta">
        <a class="btn" href="#novidades">Comprar a coleção</a>
        <a class="btn-link" href="#categorias">Ver categorias {ICON["arrow"]}</a>
      </div>
    </div>
    <button class="hero__pause" type="button" aria-pressed="false" data-pause-motion>Pausar animação</button>
  </section>

  <section class="perks" aria-label="Vantagens da loja">
    <div class="wrap">
    <ul class="perks__list" role="list">
      <li><span class="perks__icon">{ICON["truck"]}</span><span><strong>Frete grátis</strong> acima de {brl(FRETE_GRATIS)}</span></li>
      <li><span class="perks__icon">{ICON["swap"]}</span><span><strong>Troca fácil</strong> em até 7 dias</span></li>
      <li><span class="perks__icon">{ICON["gift"]}</span><span><strong>Embalagem para presente</strong> sem custo</span></li>
      <li><span class="perks__icon">{ICON["card"]}</span><span><strong>Pix ou cartão</strong> em até 3x sem juros</span></li>
    </ul>
    </div>
  </section>

{secao_categorias()}

  <div class="filterbar" data-filterbar hidden>
    <div class="wrap filterbar__in">
      <p>Mostrando: <strong data-filter-name></strong></p>
      <button class="chip" type="button" data-clear-filter>Limpar filtro {ICON["close"]}</button>
    </div>
  </div>

{secao_atual()}

  <section id="atelie" class="sec sec--atelie" aria-labelledby="t-atelie">
    <div class="wrap">
    <div class="atelie">
      <div class="atelie__intro">
        <p class="tag tag--inverse">O ateliê</p>
        <h2 id="t-atelie" class="sec__title">Uma ceramista, um forno, <em>uma fornada por mês.</em></h2>
        <p>Cada peça é torneada e esmaltada à mão em Curitiba. Por isso nenhuma é igual à outra: o esmalte escorre do seu jeito em cada queima.</p>
      </div>
      <figure class="atelie__photo">
        {foto("atelie/torno", [640, 1024], 1024, 1280, "(min-width: 1024px) 340px, 100vw", "Mãos da ceramista acertando o pé de uma tigela no torno.")}
      </figure>
      <ul class="facts" role="list">
        <li><span class="facts__num">1.240<small>°C</small></span><span>Queima em alta temperatura: o grés fica resistente, vai ao micro-ondas e à lava-louças.</span></li>
        <li><span class="facts__num">14ª<small>fornada</small></span><span>Fornadas pequenas, uma por mês. A variação de tom entre peças é parte do desenho, não defeito.</span></li>
        <li><span class="facts__num">1<small>ceramista</small></span><span>Cada peça é torneada e esmaltada à mão, do começo ao fim, pela mesma pessoa.</span></li>
      </ul>
    </div>
    </div>
  </section>

{secao_passadas()}


  <section id="ajuda" class="sec" aria-labelledby="t-ajuda">
    <div class="wrap faq">
      <header>
        <h2 id="t-ajuda" class="sec__title">Ajuda</h2>
        <p class="sec__lead">Respostas rápidas antes de comprar.</p>
      </header>
      <div class="faq__list">
        <details id="envio">
          <summary>Envio e prazos</summary>
          <p>Postamos em até 3 dias úteis, em caixa com proteção individual para cada peça. O prazo de entrega depende do CEP e aparece na sacola de uma loja real; nesta demonstração não há cálculo de frete.</p>
        </details>
        <details id="trocas">
          <summary>Trocas e devoluções</summary>
          <p>Você tem 7 dias após o recebimento para pedir troca ou devolução, como prevê o Código de Defesa do Consumidor. Se a peça chegar com dano, enviamos outra.</p>
        </details>
        <details id="cuidados">
          <summary>Cuidados com as peças</summary>
          <p>Grés queimado a 1.240 °C pode ir ao micro-ondas e à lava-louças. Evite tirar a peça da geladeira direto para o forno quente.</p>
        </details>
        <details id="pagamento">
          <summary>Formas de pagamento</summary>
          <p>Pix ou cartão de crédito em até 3x sem juros, a partir de R$ 90.</p>
        </details>
      </div>
    </div>
  </section>

</main>

<footer class="footer">
  <div class="footer__panel">
  <div class="footer__grid">
    <div class="footer__brand">
      <img src="assets/logo-mono-fundo-escuro.svg" width="101" height="40" alt="Ateliê Bruma">
      <p>Cerâmica de mesa feita à mão, em fornadas pequenas.</p>
    </div>
    <nav class="footer__col" aria-label="Loja">
      <h2>Loja</h2>
      <ul role="list">
        <li><a href="#novidades">Novidades</a></li>
        <li><a href="#categorias">Categorias</a></li>
        <li><a href="#colecoes">Coleções passadas</a></li>
      </ul>
    </nav>
    <nav class="footer__col" aria-label="Ajuda">
      <h2>Ajuda</h2>
      <ul role="list">
        <li><a href="#envio">Envio e prazos</a></li>
        <li><a href="#trocas">Trocas e devoluções</a></li>
        <li><a href="#cuidados">Cuidados com as peças</a></li>
        <li><a href="#pagamento">Pagamento</a></li>
      </ul>
    </nav>
    <p class="footer__legal">Ateliê Bruma é uma marca fictícia criada para um piloto de avaliação. Produtos, preços e políticas são exemplos e nenhuma compra é processada.</p>
  </div>
  <div class="footer__mark" aria-hidden="true"></div>
  </div>
</footer>

<div class="drawer drawer--right" id="sacola" data-drawer hidden>
  <div class="drawer__scrim" data-close></div>
  <div class="drawer__panel cart" role="dialog" aria-modal="true" aria-labelledby="t-sacola">
    <div class="drawer__head">
      <h2 id="t-sacola" class="cart__title">Sua sacola</h2>
      <button class="icon-btn" type="button" aria-label="Fechar sacola" data-close>{ICON["close"]}</button>
    </div>
    <div class="cart__ship" data-ship>
      <p data-ship-text>Faltam {brl(FRETE_GRATIS)} para o frete grátis.</p>
      <div class="cart__bar"><span data-ship-bar></span></div>
    </div>
    <ul class="cart__list" role="list" data-cart-list></ul>
    <div class="cart__empty" data-cart-empty>
      <p>Sua sacola está vazia.</p>
      <a class="btn btn--ghost" href="#novidades" data-close>Ver novidades</a>
    </div>
    <div class="cart__foot" data-cart-foot hidden>
      <p class="cart__sum"><span>Subtotal</span><strong data-cart-subtotal>R$ 0</strong></p>
      <button class="btn btn--block" type="button" data-checkout>Finalizar compra</button>
      <p class="cart__notice" data-checkout-notice role="status"></p>
    </div>
  </div>
</div>

<div class="toast" role="status" aria-live="polite" data-toast></div>

<script>window.BRUMA_FRETE_GRATIS = {FRETE_GRATIS};</script>
</body>
</html>
'''


def main() -> None:
    (ROOT / "site" / "index.html").write_text(page(), encoding="utf-8")
    print("site/index.html gerado com", len(CATALOGO), "peças")


if __name__ == "__main__":
    main()
