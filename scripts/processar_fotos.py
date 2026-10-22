#!/usr/bin/env python3
"""Recorta e otimiza as fotos do Ateliê Bruma (DES-001) para o site. Offline, só Pillow.

As imagens foram geradas por IA (ChatGPT, manualmente, pelo proprietário) a partir
dos prompts do agente eixo-graphic-designer. Os originais PNG ficam fora do
repositório (pasta do projeto / Drive); aqui entram só os derivados.

Uso: python3 scripts/processar_fotos.py <pasta_dos_originais>
A pasta tem as subpastas produtos/, categorias/, banner/, colecoes/, atelie/, og/.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "assets" / "fotos"


def crop(im: Image.Image, ratio: float, top: float = 0.5) -> Image.Image:
    """Recorta para largura/altura = ratio. top: 0 = alinha em cima, 1 = embaixo."""
    w, h = im.size
    if w / h > ratio:
        nw = round(h * ratio)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = round(w / ratio)
    y = round((h - nh) * top)
    return im.crop((0, y, w, y + nh))


def salvar(im: Image.Image, dest: Path, larguras: list[int], jpg: bool = True) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    for lw in larguras:
        r = im.resize((lw, round(lw * im.height / im.width)), Image.LANCZOS)
        r.save(dest.with_name(f"{dest.stem}-{lw}.webp"), "WEBP", quality=80, method=6)
    if jpg:  # fallback, maior largura
        lw = larguras[-1]
        r = im.resize((lw, round(lw * im.height / im.width)), Image.LANCZOS)
        r.save(dest.with_name(f"{dest.stem}-{lw}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)


def main(src: Path) -> None:
    for f in sorted((src / "produtos").glob("*.png")):
        # 2:3 -> 4:5; corta mais em cima (céu vazio) que embaixo (mesa)
        salvar(crop(Image.open(f).convert("RGB"), 4 / 5, top=0.75), OUT / "produtos" / f.stem, [480, 800])
    for f in sorted((src / "categorias").glob("*.png")):
        salvar(crop(Image.open(f).convert("RGB"), 1), OUT / "categorias" / f.stem, [400, 640])
    b = src / "banner"
    salvar(Image.open(b / "banner-desktop.png").convert("RGB"), OUT / "banner" / "desktop", [1024, 1536])
    salvar(crop(Image.open(b / "banner-celular.png").convert("RGB"), 1), OUT / "banner" / "celular", [640, 960])
    for f in sorted((src / "colecoes").glob("*.png")):
        salvar(Image.open(f).convert("RGB"), OUT / "colecoes" / f.stem, [800, 1536])
    for f in sorted((src / "atelie").glob("*.png")):
        im = Image.open(f).convert("RGB")
        salvar(crop(im, 4 / 5) if im.height > im.width else im, OUT / "atelie" / f.stem, [640, 1024])
    og = crop(Image.open(src / "og" / "compartilhar.png").convert("RGB"), 1200 / 630)
    (OUT / "og").mkdir(parents=True, exist_ok=True)
    og.resize((1200, 630), Image.LANCZOS).save(OUT / "og" / "compartilhar.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"ok: {sum(1 for p in OUT.rglob('*') if p.is_file())} arquivos, {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
