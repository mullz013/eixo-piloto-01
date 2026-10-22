#!/usr/bin/env python3
"""Gera as ilustrações SVG das peças do Ateliê Bruma (marca fictícia).

Cada peça é um sólido de revolução descrito por um perfil (y, raio), desenhado
em perspectiva leve, com esmalte por coleção, pé de argila crua, textura de grés
e sombra. Saída: site/assets/pecas/<colecao>-<forma>.svg (fundo transparente).

Uso: python3 scripts/gerar_pecas.py
"""
from __future__ import annotations

import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "assets" / "pecas"

W, H = 400, 500
CX = 200

# ---------------------------------------------------------------- esmaltes
GLAZES = {
    "nevoa": {
        "dark": "#6E797D", "mid": "#9DA8AB", "light": "#C3CACA", "hi": "#DDE1DE",
        "in_top": "#C9CFCD", "in_bot": "#8C9597",
        "clay": "#CDB89B", "clay_dark": "#A89276",
        "speck": "#3E3A35", "speck_density": 0.79,
        "layer": "#EEF0EC", "layer_opacity": 0.62, "layer_mode": "top",
    },
    "terra": {
        "dark": "#3F1E11", "mid": "#7A3B22", "light": "#A65A38", "hi": "#C98762",
        "in_top": "#8E4A2C", "in_bot": "#4A2414",
        "clay": "#A9795A", "clay_dark": "#80553A",
        "speck": "#1F120B", "speck_density": 0.77,
        "layer": "#C29267", "layer_opacity": 0.75, "layer_mode": "top",
    },
    "sal": {
        "dark": "#B5AFA4", "mid": "#DDD8CF", "light": "#F2EFE9", "hi": "#FFFFFF",
        "in_top": "#F0EDE7", "in_bot": "#C9C3B8",
        "clay": "#D6C3A6", "clay_dark": "#B5A07F",
        "speck": "#5C5348", "speck_density": 0.81,
        "layer": "#2D4C70", "layer_opacity": 1.0, "layer_mode": "rim",
    },
}

# ---------------------------------------------------------------- formas
# perfil: lista (y, raio) de cima para baixo; k = achatamento da elipse
SHAPES = {
    "caneca":   {"k": 0.24, "open": True,  "profile": [(196, 74), (214, 75), (300, 77), (380, 76), (414, 71), (430, 66)], "handle": "mug"},
    "xicara":   {"k": 0.26, "open": True,  "profile": [(282, 64), (300, 63), (340, 56), (372, 44), (386, 38)], "handle": "cup", "saucer": True},
    "tigela":   {"k": 0.32, "open": True,  "profile": [(286, 128), (306, 125), (348, 110), (384, 82), (404, 58), (414, 50)]},
    "prato":    {"k": 0.36, "open": True,  "plate": True, "profile": [(352, 156), (360, 154), (372, 136), (382, 98), (386, 94)]},
    "travessa": {"k": 0.30, "open": True,  "plate": True, "profile": [(338, 168), (348, 165), (374, 150), (396, 124), (402, 118)], "lugs": True},
    "garrafa":  {"k": 0.22, "open": True,  "narrow": True, "profile": [(132, 22), (140, 23), (150, 18), (196, 18), (226, 38), (262, 78), (318, 94), (378, 86), (414, 66), (430, 58)]},
    "jarra":    {"k": 0.24, "open": True,  "profile": [(178, 62), (196, 61), (236, 66), (304, 82), (378, 86), (416, 76), (430, 70)], "handle": "jug", "spout": True},
    "copo":     {"k": 0.24, "open": True,  "profile": [(236, 60), (260, 60), (380, 56), (420, 53), (430, 51)]},
    "ramequim": {"k": 0.30, "open": True,  "profile": [(330, 92), (346, 91), (390, 84), (414, 72), (424, 66)]},
    "bojudo":   {"k": 0.24, "open": True,  "narrow": True, "profile": [(196, 30), (206, 31), (226, 46), (262, 96), (322, 118), (384, 104), (418, 76), (430, 66)]},
}


def fmt(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def catmull(points: list[tuple[float, float]]) -> str:
    """Curva suave (Catmull-Rom -> Bézier cúbica) passando pelos pontos."""
    d = []
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}")
    return " ".join(d)


def silhouette(profile, k) -> str:
    right = [(CX + r, y) for y, r in profile]
    left = [(CX - r, y) for y, r in reversed(profile)]
    yt, rt = profile[0]
    yb, rb = profile[-1]
    d = f"M{fmt(right[0][0])} {fmt(right[0][1])} " + catmull(right)
    d += f" A{fmt(rb)} {fmt(rb * k)} 0 0 1 {fmt(CX - rb)} {fmt(yb)} "
    d += catmull(left)
    d += f" A{fmt(rt)} {fmt(rt * k)} 0 0 1 {fmt(CX + rt)} {fmt(yt)} Z"
    return d


def radius_at(profile, y) -> float:
    for (y0, r0), (y1, r1) in zip(profile, profile[1:]):
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0) if y1 != y0 else 0
            return r0 + (r1 - r0) * t
    return profile[-1][1]


def wavy_band(y, R, k, rng, amp=1.6, drips=0, drip_len=(8, 22), below=True) -> str:
    """Região abaixo (ou acima) de uma linha de esmalte que segue a frente da peça."""
    n = 48
    pts = []
    drip_pos = [rng.uniform(0.12, 0.88) for _ in range(drips)]
    drip_l = [rng.uniform(*drip_len) for _ in range(drips)]
    for i in range(n + 1):
        t = i / n
        ang = math.pi * t  # 0 = esquerda, pi = direita, passando pela frente
        x = CX - R * math.cos(ang)
        yy = y + R * k * math.sin(ang)
        yy += amp * math.sin(t * 17 + rng.random()) + amp * 0.6 * math.sin(t * 41)
        for p, L in zip(drip_pos, drip_l):
            yy += L * math.exp(-((t - p) ** 2) / 0.0009)
        pts.append((x, yy))
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])} " + " ".join(f"L{fmt(x)} {fmt(yy)}" for x, yy in pts[1:])
    edge = H if below else 0
    d += f" L{fmt(CX + R)} {edge} L{fmt(CX - R)} {edge} Z"
    return d


def crop_box(s) -> str:
    """Enquadra a peça num quadro 4:5 com a base sempre a 80% da altura."""
    prof, k = s["profile"], s["k"]
    maxr = max(r for _, r in prof)
    if s.get("saucer"):
        maxr = max(maxr, 126)
    extra = 74 if s.get("handle") in ("mug", "jug") else (40 if s.get("handle") else 0)
    extra = max(extra, 30 if s.get("spout") else 0)
    yb = 404 if s.get("saucer") else prof[-1][0]
    top = min(y for y, _ in prof) - prof[0][1] * k - (16 if s.get("spout") else 0)
    cw = (2 * (maxr + extra) + 36) * 1.3
    wc = cw
    while True:
        hc = wc * 1.25
        y0 = yb - 0.80 * hc
        if top - y0 >= 0.1 * hc:
            break
        wc += 4
    x0 = CX - wc / 2
    return f"{fmt(x0)} {fmt(y0)} {fmt(wc)} {fmt(hc)}"


def piece_svg(collection: str, shape_key: str, seed: int) -> str:
    g = GLAZES[collection]
    s = SHAPES[shape_key]
    k = s["k"]
    prof = s["profile"]
    rng = random.Random(seed)
    uid = f"{collection[0]}{shape_key[:3]}"
    yt, rt = prof[0]
    yb, rb = prof[-1]
    sil = silhouette(prof, k)
    ymin = min(y for y, _ in prof)
    span = yb - ymin

    defs = [
        f'<linearGradient id="{uid}g" x1="0" x2="1" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{g["dark"]}"/><stop offset=".16" stop-color="{g["mid"]}"/>'
        f'<stop offset=".34" stop-color="{g["light"]}"/><stop offset=".42" stop-color="{g["hi"]}"/>'
        f'<stop offset=".56" stop-color="{g["light"]}"/><stop offset=".8" stop-color="{g["mid"]}"/>'
        f'<stop offset="1" stop-color="{g["dark"]}"/></linearGradient>',
        f'<linearGradient id="{uid}ao" x1="0" x2="0" y1="0" y2="1">'
        f'<stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".7" stop-color="#000" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>',
        f'<linearGradient id="{uid}in" x1="0" x2="0" y1="0" y2="1">'
        f'<stop offset="0" stop-color="{g["in_bot"]}"/><stop offset=".55" stop-color="{g["in_top"]}"/>'
        f'<stop offset="1" stop-color="{g["light"]}"/></linearGradient>',
        f'<linearGradient id="{uid}cl" x1="0" x2="1"><stop offset="0" stop-color="{g["clay_dark"]}"/>'
        f'<stop offset=".4" stop-color="{g["clay"]}"/><stop offset="1" stop-color="{g["clay_dark"]}"/></linearGradient>',
        f'<clipPath id="{uid}c"><path d="{sil}"/></clipPath>',
        f'<filter id="{uid}sp" x="0" y="0" width="1" height="1"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="{seed}"/>'
        f'<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  14 0 0 0 {fmt(-14 * g["speck_density"])}"/>'
        f'<feComposite operator="in" in2="SourceGraphic"/></filter>',
        f'<filter id="{uid}bl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>',
        f'<filter id="{uid}hl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>',
    ]

    body = []
    # sombra
    body.append(f'<ellipse cx="{CX + 8}" cy="{fmt(yb + 4)}" rx="{fmt(rb * 1.5 + 14)}" ry="{fmt(rb * k * 1.5 + 6)}" fill="#2A241D" opacity=".26" filter="url(#{uid}bl)"/>')

    # pires
    if s.get("saucer"):
        sy, sr, sk = 392, 118, 0.27
        body.append(f'<ellipse cx="{CX + 6}" cy="{sy + 12}" rx="{sr + 8}" ry="{fmt(sr * sk + 4)}" fill="#2A241D" opacity=".22" filter="url(#{uid}bl)"/>')
        body.append(f'<path d="M{CX - sr} {sy} A{sr} {fmt(sr * sk)} 0 0 0 {CX + sr} {sy} L{CX + sr - 10} {sy + 8} A{sr - 10} {fmt((sr - 10) * sk)} 0 0 1 {CX - sr + 10} {sy + 8} Z" fill="url(#{uid}cl)"/>')
        body.append(f'<ellipse cx="{CX}" cy="{sy}" rx="{sr}" ry="{fmt(sr * sk)}" fill="url(#{uid}g)"/>')
        body.append(f'<ellipse cx="{CX}" cy="{sy + 2}" rx="{sr - 26}" ry="{fmt((sr - 26) * sk)}" fill="url(#{uid}in)" opacity=".75"/>')

    # alça (atrás do corpo, presa na lateral direita)
    handle = s.get("handle")
    if handle:
        if handle == "mug":
            y1, y2, out = 236, 366, 62
        elif handle == "cup":
            y1, y2, out = 300, 352, 34
        else:
            y1, y2, out = 214, 372, 70
        x1 = CX + radius_at(prof, y1) - 10
        x2 = CX + radius_at(prof, y2) - 10
        hp = f"M{fmt(x1)} {y1} C{fmt(x1 + out * 1.1)} {y1 - 8} {fmt(x2 + out * 1.15)} {y2 - 30} {fmt(x2)} {y2}"
        sw = 17 if handle != "cup" else 11
        body.append(f'<path d="{hp}" fill="none" stroke="{g["dark"]}" stroke-width="{sw}" stroke-linecap="round"/>')
        body.append(f'<path d="{hp}" fill="none" stroke="{g["mid"]}" stroke-width="{sw - 6}" stroke-linecap="round" transform="translate(-1.5 -1.5)"/>')
        body.append(f'<path d="{hp}" fill="none" stroke="{g["light"]}" stroke-width="{max(2, sw // 5)}" stroke-linecap="round" opacity=".8" transform="translate(-3 -3)"/>')

    # orelhas da travessa
    if s.get("lugs"):
        for sign in (-1, 1):
            x = CX + sign * (rt + 2)
            body.append(f'<ellipse cx="{fmt(x)}" cy="{yt + 6}" rx="16" ry="7" fill="{g["mid"]}" stroke="{g["dark"]}" stroke-width="1"/>')

    # corpo
    body.append(f'<path d="{sil}" fill="url(#{uid}g)"/>')
    clip = f'clip-path="url(#{uid}c)"'
    inner = []
    # camada de esmalte (névoa / terra) ou borda (sal)
    if g["layer_mode"] == "top":
        ly = ymin + span * (0.42 if not s.get("plate") else 0.2)
        R = max(r for _, r in prof) + 12
        inner.append(f'<path d="{wavy_band(ly, R, k, rng, amp=2.2, drips=5, drip_len=(10, 34), below=False)}" fill="{g["layer"]}" opacity="{g["layer_opacity"]}"/>')
    else:
        ly = yt + (9 if not s.get("plate") else 6)
        R = rt + 12
        inner.append(f'<path d="{wavy_band(ly, R, k, rng, amp=0.8, drips=0 if s.get("plate") else 3, drip_len=(4, 12), below=False)}" fill="{g["layer"]}" opacity="{g["layer_opacity"]}"/>')
    # pé de argila crua
    foot_y = yb - (13 if not s.get("plate") else 6)
    R = rb + 16
    inner.append(f'<path d="{wavy_band(foot_y, radius_at(prof, foot_y), k, rng, amp=0.9)}" fill="url(#{uid}cl)"/>')
    # textura de grés, sombreado e brilho
    inner.append(f'<rect width="{W}" height="{H}" fill="{g["speck"]}" filter="url(#{uid}sp)" opacity=".45"/>')
    inner.append(f'<rect x="0" y="{ymin}" width="{W}" height="{span + 4}" fill="url(#{uid}ao)"/>')
    hx = CX - max(r for _, r in prof) * 0.34
    inner.append(f'<ellipse cx="{fmt(hx)}" cy="{fmt(ymin + span * 0.5)}" rx="7" ry="{fmt(span * 0.32)}" fill="#fff" opacity=".28" filter="url(#{uid}hl)"/>')
    body.append(f'<g {clip}>' + "".join(inner) + "</g>")

    # boca: lábio + interior
    lip = g["layer"] if g["layer_mode"] == "rim" else g["light"]
    if s.get("narrow"):
        body.append(f'<ellipse cx="{CX}" cy="{yt}" rx="{rt}" ry="{fmt(rt * k)}" fill="{lip}"/>')
        body.append(f'<ellipse cx="{CX}" cy="{fmt(yt + 0.5)}" rx="{fmt(rt * 0.66)}" ry="{fmt(rt * k * 0.62)}" fill="#1B1714"/>')
    elif s.get("plate"):
        body.append(f'<ellipse cx="{CX}" cy="{yt}" rx="{rt}" ry="{fmt(rt * k)}" fill="{lip}"/>')
        body.append(f'<ellipse cx="{CX}" cy="{fmt(yt + 1.5)}" rx="{fmt(rt - 6)}" ry="{fmt((rt - 6) * k)}" fill="url(#{uid}g)"/>')
        wr = rt * 0.62
        body.append(f'<ellipse cx="{CX}" cy="{fmt(yt + 6)}" rx="{fmt(wr)}" ry="{fmt(wr * k)}" fill="url(#{uid}in)" opacity=".5"/>')
        body.append(f'<ellipse cx="{CX}" cy="{fmt(yt + 6)}" rx="{fmt(wr)}" ry="{fmt(wr * k)}" fill="none" stroke="{g["dark"]}" stroke-opacity=".35" stroke-width="1.2"/>')
        body.append(f'<rect width="{W}" height="{H}" fill="{g["speck"]}" filter="url(#{uid}sp)" opacity=".4" clip-path="url(#{uid}lip)"/>')
        defs.append(f'<clipPath id="{uid}lip"><ellipse cx="{CX}" cy="{yt}" rx="{rt}" ry="{fmt(rt * k)}"/></clipPath>')
    else:
        body.append(f'<ellipse cx="{CX}" cy="{yt}" rx="{rt}" ry="{fmt(rt * k)}" fill="{lip}"/>')
        ir = rt - 5.5
        body.append(f'<ellipse cx="{CX}" cy="{fmt(yt + 0.8)}" rx="{fmt(ir)}" ry="{fmt(ir * k)}" fill="url(#{uid}in)"/>')
        body.append(f'<rect width="{W}" height="{H}" fill="{g["speck"]}" filter="url(#{uid}sp)" opacity=".35" clip-path="url(#{uid}lip)"/>')
        defs.append(f'<clipPath id="{uid}lip"><ellipse cx="{CX}" cy="{yt}" rx="{rt}" ry="{fmt(rt * k)}"/></clipPath>')
        if g["layer_mode"] == "rim":
            body.append(f'<ellipse cx="{CX}" cy="{fmt(yt + 0.8)}" rx="{fmt(ir)}" ry="{fmt(ir * k)}" fill="none" stroke="{g["layer"]}" stroke-width="2" opacity=".55"/>')

    # bico da jarra
    if s.get("spout"):
        x0 = CX - rt
        body.append(f'<path d="M{fmt(x0 + 10)} {yt - 9} C{fmt(x0 - 6)} {yt - 14} {fmt(x0 - 22)} {yt - 16} {fmt(x0 - 26)} {yt - 11} C{fmt(x0 - 18)} {yt + 2} {fmt(x0 - 6)} {yt + 12} {fmt(x0 + 12)} {yt + 13} Z" fill="{lip}"/>')
        body.append(f'<path d="M{fmt(x0 + 8)} {yt - 5} C{fmt(x0 - 4)} {yt - 8} {fmt(x0 - 14)} {yt - 10} {fmt(x0 - 18)} {yt - 8} C{fmt(x0 - 10)} {yt + 1} {fmt(x0 - 2)} {yt + 6} {fmt(x0 + 10)} {yt + 7} Z" fill="url(#{uid}in)"/>')

    vb = crop_box(s)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="400" height="500">'
        f'<!-- Ateliê Bruma (marca fictícia) | ilustração gerada por scripts/gerar_pecas.py -->'
        f'<defs>{"".join(defs)}</defs>{"".join(body)}</svg>\n'
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    seed = 7
    for coll in GLAZES:
        for shape in SHAPES:
            seed += 3
            (OUT / f"{coll}-{shape}.svg").write_text(piece_svg(coll, shape, seed), encoding="utf-8")
    print(f"{len(GLAZES) * len(SHAPES)} ilustrações em {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
