#!/usr/bin/env python3
"""QA-001 · Ateliê Bruma (piloto-01) · testes E2E reais com Playwright (Python, sync API).

Executa no Chromium local, contra file://.../site/index.html. Não altera site/, scripts/ nem tests/.
Saída: evidence/QA-001/results.json + screenshots em evidence/QA-001/shots/.
Uso: python3 evidence/QA-001/qa_test.py [--axe /caminho/axe.min.js]
"""
import json
import re
import os
import sys
import time
import traceback
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
URL = (ROOT / "site" / "index.html").as_uri()
if "--base-url" in sys.argv:
    URL = sys.argv[sys.argv.index("--base-url") + 1]
TAG = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else "file"
SHOTS = OUT / "shots" / TAG
SHOTS.mkdir(parents=True, exist_ok=True)
BASE = URL.rsplit("/", 1)[0] + "/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
AXE = None
if "--axe" in sys.argv:
    AXE = Path(sys.argv[sys.argv.index("--axe") + 1])

WIDTHS = [(320, 568), (375, 667), (414, 896), (768, 1024), (1024, 768), (1440, 900)]
RESULTS = []


def record(cid, title, status, details=None):
    RESULTS.append({"id": cid, "title": title, "status": status, "details": details})
    print(f"[{status}] {cid} {title}" + (f" :: {json.dumps(details, ensure_ascii=False)[:400]}" if details else ""))


def run(cid, title):
    """Decorator: executes the check; exceptions become FAIL (assertion) or ERROR (other)."""
    def deco(fn):
        try:
            res = fn()
            if isinstance(res, tuple):
                status, details = res
            else:
                status, details = ("PASS", res)
            record(cid, title, status, details)
        except AssertionError as e:
            record(cid, title, "FAIL", {"assert": str(e)})
        except Exception as e:  # noqa: BLE001
            record(cid, title, "ERROR", {"error": repr(e), "trace": traceback.format_exc()[-1500:]})
        return fn
    return deco


def new_page(browser, w, h, js=True, motion="no-preference", collect=None):
    ctx = browser.new_context(viewport={"width": w, "height": h}, java_script_enabled=js,
                              reduced_motion=motion, device_scale_factor=1)
    page = ctx.new_page()
    if collect is not None:
        page.on("console", lambda m: m.type in ("error", "warning") and collect.append({"type": m.type, "text": m.text}))
        page.on("pageerror", lambda e: collect.append({"type": "pageerror", "text": str(e)}))
        page.on("requestfailed", lambda r: collect.append({"type": "requestfailed", "url": r.url, "err": r.failure}))
    page.goto(URL)
    page.wait_for_load_state("load")
    return ctx, page


def scroll_through(page):
    h = page.evaluate("document.documentElement.scrollHeight")
    vh = page.evaluate("innerHeight")
    y = 0
    while y < h:
        page.evaluate(f"window.scrollTo(0,{y})")
        page.wait_for_timeout(120)
        y += int(vh * 0.6)
        h = page.evaluate("document.documentElement.scrollHeight")
    # lazy images inside horizontal carousels: bring each track into view, then scroll it to the end
    n = page.evaluate("document.querySelectorAll('.carousel__track').length")
    for i in range(n):
        page.evaluate(f"(() => {{ const t = document.querySelectorAll('.carousel__track')[{i}]; t.scrollIntoView({{block: 'center'}}); t.style.scrollBehavior='auto'; t.scrollLeft = t.scrollWidth; }})()")
        page.wait_for_timeout(400)
    page.evaluate("""() => document.querySelectorAll('.carousel__track').forEach(t => { t.scrollLeft = 0; t.style.scrollBehavior=''; })""")
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(300)


def settle_scroll(page, expr="window.scrollY", timeout=3000):
    last, stable, t0 = None, 0, time.time()
    while time.time() - t0 < timeout / 1000:
        v = page.evaluate(expr)
        stable = stable + 1 if v == last else 0
        if stable >= 3:
            return v
        last = v
        page.wait_for_timeout(80)
    return page.evaluate(expr)


BROKEN_IMGS_JS = """() => [...document.images].filter(i => !i.closest('[hidden]'))
  .map(i => ({src: i.currentSrc || i.src, complete: i.complete, nw: i.naturalWidth, lazy: i.loading}))
  .filter(i => !i.complete || i.nw === 0)"""

OVERFLOW_JS = """() => {
  const de = document.documentElement, vw = de.clientWidth;
  const offenders = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    // skip descendants of horizontally scrolling containers (carousel tracks) and of hidden drawers
    let p = el.parentElement, clipped = false;
    while (p && p !== document.body) {
      const cs = getComputedStyle(p);
      if (cs.overflowX !== 'visible' && cs.overflowX !== 'clip' ) { clipped = true; break; }
      if (cs.overflowX === 'clip') { clipped = true; break; }
      p = p.parentElement;
    }
    if (clipped) return;
    if (r.right > vw + 1 || r.left < -1) offenders.push({tag: el.tagName, cls: el.className && el.className.baseVal === undefined ? el.className : '', left: Math.round(r.left), right: Math.round(r.right)});
  });
  return {scrollWidth: de.scrollWidth, clientWidth: vw, bodyScrollWidth: document.body.scrollWidth, offenders: offenders.slice(0, 10)};
}"""

MARGINS_JS = """() => {
  const vw = document.documentElement.clientWidth;
  const out = [];
  const sel = ['.announce', '.header__in', '.hero__copy', '.perks .wrap', '#categorias .wrap', '#categorias .sec__head',
               '#novidades .sec__head', '#atelie .wrap', '#colecoes .sec__intro', '.past .sec__head', '.faq', '.footer__panel', '.footer__grid'];
  sel.forEach(s => document.querySelectorAll(s).forEach((el, i) => {
    if (el.closest('[hidden]')) return;
    const r = el.getBoundingClientRect(); if (!r.width) return;
    const cs = getComputedStyle(el);
    const L = r.left + parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth);
    const R = vw - (r.right - parseFloat(cs.paddingRight) - parseFloat(cs.borderRightWidth));
    out.push({sel: s + (i ? `[${i}]` : ''), left: +L.toFixed(1), right: +R.toFixed(1), diff: +(L - R).toFixed(1)});
  }));
  // first card of each carousel vs. section heading (left alignment)
  document.querySelectorAll('[data-carousel]').forEach(c => {
    const li = c.querySelector('.carousel__track > li:not([hidden])'); if (!li) return;
    out.push({sel: 'first-card:' + c.dataset.name, left: +li.getBoundingClientRect().left.toFixed(1), right: null, diff: null});
  });
  return out;
}"""

FOCUS_VISIBLE_JS = """() => {
  const el = document.activeElement; if (!el || el === document.body) return null;
  const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
  const header = document.querySelector('[data-header]'); const hb = header ? header.getBoundingClientRect().bottom : 0;
  const inHeader = header && header.contains(el);
  const inDrawer = !!el.closest('[data-drawer]');
  const outline = cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0;
  const shadow = cs.boxShadow && cs.boxShadow !== 'none';
  return {tag: el.tagName, text: (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\\s+/g,' ').slice(0, 50),
          cls: typeof el.className === 'string' ? el.className.slice(0,40) : '',
          outline: outline ? `${cs.outlineStyle} ${cs.outlineWidth} ${cs.outlineColor} off ${cs.outlineOffset}` : null,
          shadow: shadow ? cs.boxShadow.slice(0, 60) : null, visibleIndicator: outline || shadow,
          top: Math.round(r.top), bottom: Math.round(r.bottom), w: Math.round(r.width), h: Math.round(r.height),
          inViewport: r.bottom > 0 && r.top < innerHeight && r.width > 0,
          obscuredByHeader: !inHeader && !inDrawer && r.bottom <= hb + 1 && r.height > 0,
          partlyUnderHeader: !inHeader && !inDrawer && r.top < hb - 1};
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True)
        meta = {"url": URL, "chromium": browser.version, "playwright_python": "1.64.0", "axe": str(AXE) if AXE else None}

        # ---------- T01 console errors + broken images after lazy-scroll (375 & 1440) ----------
        for (w, h) in [(375, 667), (1440, 900)]:
            logs = []
            ctx, page = new_page(browser, w, h, collect=logs)
            scroll_through(page)

            @run(f"T01-console-{w}", f"Sem erros de console/pageerror/requestfailed ({w}px, página percorrida)")
            def _():
                errs = [l for l in logs if l["type"] in ("error", "pageerror", "requestfailed")]
                assert not errs, json.dumps(errs, ensure_ascii=False)[:800]
                return {"warnings": [l for l in logs if l["type"] == "warning"]}

            @run(f"T02-images-{w}", f"Nenhuma imagem quebrada depois de rolar até as lazy ({w}px)")
            def _():
                broken = page.evaluate(BROKEN_IMGS_JS)
                total = page.evaluate("document.images.length")
                assert not broken, json.dumps(broken)[:800]
                return {"images_checked": total}

            page.screenshot(path=str(SHOTS / f"pagina-{w}-full.png"), full_page=True)
            ctx.close()

        # ---------- T03 horizontal overflow at all widths ----------
        for (w, h) in WIDTHS:
            ctx, page = new_page(browser, w, h)
            scroll_through(page)

            @run(f"T03-overflow-{w}", f"Sem rolagem horizontal da página em {w}px")
            def _():
                o = page.evaluate(OVERFLOW_JS)
                page.evaluate("window.scrollTo(500, 0)")
                sx = page.evaluate("window.scrollX")
                o["scrollX_after_scrollTo500"] = sx
                assert o["scrollWidth"] <= o["clientWidth"] and sx == 0, json.dumps(o)
                return o
            ctx.close()

        # ---------- T04 symmetric mobile margins ----------
        for (w, h) in [(320, 568), (375, 667), (414, 896), (768, 1024)]:
            ctx, page = new_page(browser, w, h)
            page.wait_for_timeout(300)

            @run(f"T04-margins-{w}", f"Margens horizontais simétricas no celular/tablet ({w}px, tolerância 1px)")
            def _():
                m = page.evaluate(MARGINS_JS)
                bad = [x for x in m if x["diff"] is not None and abs(x["diff"]) > 1]
                assert not bad, json.dumps(bad, ensure_ascii=False)
                return m
            ctx.close()

        # ---------- T05 hamburger menu (375) ----------
        ctx, page = new_page(browser, 375, 667)
        page.wait_for_timeout(200)
        btn = page.get_by_role("button", name="Abrir menu")

        @run("T05a-menu-open", "Menu: botão 'Abrir menu' visível; abre gaveta, aria-expanded=true, foco dentro do painel")
        def _():
            assert btn.is_visible(), "botão hambúrguer invisível em 375"
            assert not page.locator("nav.nav").is_visible(), "nav desktop visível no celular"
            btn.click()
            page.wait_for_timeout(450)
            assert page.locator("#menu").is_visible(), "gaveta não ficou visível"
            assert btn.get_attribute("aria-expanded") == "true"
            inside = page.evaluate("!!document.activeElement.closest('#menu .drawer__panel')")
            assert inside, "foco não entrou no painel"
            inert = page.evaluate("document.querySelector('#conteudo').hasAttribute('inert')")
            assert inert, "conteúdo de fundo não ficou inert"
            page.screenshot(path=str(SHOTS / "menu-aberto-375.png"))
            return {"focused": page.evaluate(FOCUS_VISIBLE_JS)}

        @run("T05b-menu-trap", "Menu: Tab/Shift+Tab ficam presos no painel (40 Tabs)")
        def _():
            escaped = []
            for i in range(40):
                page.keyboard.press("Tab")
                if not page.evaluate("!!document.activeElement.closest('#menu .drawer__panel')"):
                    escaped.append(i)
            for i in range(5):
                page.keyboard.press("Shift+Tab")
                if not page.evaluate("!!document.activeElement.closest('#menu .drawer__panel')"):
                    escaped.append(f"shift{i}")
            assert not escaped, f"foco saiu do painel em {escaped}"

        @run("T05c-menu-escape", "Menu: Escape fecha, aria-expanded=false, foco volta ao botão, gaveta hidden")
        def _():
            page.keyboard.press("Escape")
            page.wait_for_timeout(450)
            assert btn.get_attribute("aria-expanded") == "false"
            assert page.evaluate("document.querySelector('#menu').hidden"), "gaveta não ficou hidden"
            assert page.evaluate("document.activeElement.matches('[data-open-menu]')"), "foco não voltou ao botão"
            assert not page.evaluate("document.querySelector('#conteudo').hasAttribute('inert')")

        @run("T05d-menu-close-x-scrim", "Menu: fecha pelo X e pelo toque fora (scrim)")
        def _():
            btn.click(); page.wait_for_timeout(450)
            page.get_by_role("button", name="Fechar menu").click(); page.wait_for_timeout(450)
            assert page.evaluate("document.querySelector('#menu').hidden"), "X não fechou"
            btn.click(); page.wait_for_timeout(450)
            page.mouse.click(370, 400)  # área do scrim à direita do painel
            page.wait_for_timeout(450)
            assert page.evaluate("document.querySelector('#menu').hidden"), "scrim não fechou"

        @run("T05e-menu-anchor", "Menu: link de âncora (Ajuda) fecha a gaveta e navega")
        def _():
            btn.click(); page.wait_for_timeout(450)
            link = page.locator("#menu a[href='#ajuda']").first
            link.click()
            page.wait_for_timeout(450)
            settle_scroll(page)
            assert page.evaluate("document.querySelector('#menu').hidden"), "gaveta não fechou"
            assert page.evaluate("location.hash") == "#ajuda"
            top = page.evaluate("document.querySelector('#t-ajuda').getBoundingClientRect().top")
            hb = page.evaluate("document.querySelector('[data-header]').getBoundingClientRect().bottom")
            assert top >= hb - 1 and top < 667, f"título em {top}, header termina em {hb}"
            return {"title_top": top, "header_bottom": hb}

        @run("T05f-menu-category", "Menu: categoria filtra as vitrines e mostra 'Mostrando' + 'Limpar filtro'")
        def _():
            btn.click(); page.wait_for_timeout(450)
            f = page.locator("#menu [data-filter]").first
            label = f.get_attribute("data-label")
            f.click(); page.wait_for_timeout(600)
            assert page.evaluate("document.querySelector('#menu').hidden"), "gaveta não fechou após filtro"
            bar = page.locator("[data-filterbar]")
            assert bar.is_visible(), "barra de filtro não apareceu"
            txt = bar.inner_text()
            visible = page.evaluate("document.querySelectorAll('.carousel__track > li:not([hidden])').length")
            total = page.evaluate("document.querySelectorAll('.carousel__track > li').length")
            assert 0 < visible < total, f"visíveis {visible}/{total}"
            page.screenshot(path=str(SHOTS / "filtro-375.png"))
            page.locator("[data-clear-filter]").click(); page.wait_for_timeout(500)
            after = page.evaluate("document.querySelectorAll('.carousel__track > li:not([hidden])').length")
            assert after == total and not bar.is_visible()
            return {"filter": label, "bar": txt.strip(), "visible": visible, "total": total}
        ctx.close()

        @run("T05g-menu-desktop", "1440px: hambúrguer oculto, nav principal visível")
        def _():
            c, pg = new_page(browser, 1440, 900)
            try:
                assert not pg.get_by_role("button", name="Abrir menu").is_visible()
                assert pg.locator("nav.nav").is_visible()
                return {"links": pg.locator("nav.nav a").all_inner_texts()}
            finally:
                c.close()

        # ---------- T06 nav anchors (desktop, reduced motion for deterministic scroll) ----------
        ctx, page = new_page(browser, 1440, 900, motion="reduce")
        hrefs = page.evaluate("[...document.querySelectorAll('nav.nav a[href^=\"#\"]')].map(a=>({href:a.getAttribute('href'), filter:a.hasAttribute('data-filter'), text:a.textContent.trim()}))")
        for item in hrefs:
            @run(f"T06-anchor-{item['href']}-{item['text'][:12]}", f"Nav desktop '{item['text']}' -> {item['href']}")
            def _(item=item):
                page.evaluate("window.scrollTo(0,0)")
                page.locator(f"nav.nav a[href='{item['href']}']", has_text=item["text"]).first.click()
                page.wait_for_timeout(300)
                settle_scroll(page)
                tgt = item["href"][1:]
                info = page.evaluate("""(id) => { const t = document.getElementById(id); const h = t.querySelector('h2,h3') || t;
                    const r = h.getBoundingClientRect(); const hb = document.querySelector('[data-header]').getBoundingClientRect().bottom;
                    return {hash: location.hash, top: Math.round(r.top), hb: Math.round(hb), hidden: !!t.closest('[hidden]')}; }""", tgt)
                if not item["filter"]:
                    assert info["hash"] == item["href"], info
                assert not info["hidden"], info
                assert info["top"] >= info["hb"] - 1 and info["top"] < 900, info
                if item["filter"]:
                    page.locator("[data-clear-filter]").click(); page.wait_for_timeout(200)
                return info
        ctx.close()

        # ---------- T07 deep links + unknown hash + back ----------
        for frag in ["#colecoes", "#colecao-terra", "#colecao-sal", "#ajuda", "#naoexiste"]:
            @run(f"T07-deeplink-{frag}", f"Link profundo index.html{frag} (375px)")
            def _(frag=frag):
                logs = []
                c = browser.new_context(viewport={"width": 375, "height": 667})
                pg = c.new_page()
                pg.on("pageerror", lambda e: logs.append(str(e)))
                pg.goto(URL + frag); pg.wait_for_load_state("load"); pg.wait_for_timeout(600)
                try:
                    if frag == "#naoexiste":
                        y = pg.evaluate("scrollY")
                        assert y == 0 and not logs, {"scrollY": y, "errors": logs}
                        return {"scrollY": y}
                    info = pg.evaluate("""(id) => { const t = document.getElementById(id); const h = t.querySelector('h2,h3') || t;
                        const r = h.getBoundingClientRect(); const hb = document.querySelector('[data-header]').getBoundingClientRect().bottom;
                        return {top: Math.round(r.top), hb: Math.round(hb)}; }""", frag[1:])
                    assert info["top"] >= info["hb"] - 1 and info["top"] < 667, info
                    return info
                finally:
                    c.close()

        @run("T07-back", "Voltar do navegador após âncora retorna à posição anterior sem recarregar")
        def _():
            c, pg = new_page(browser, 1440, 900, motion="reduce")
            try:
                pg.evaluate("window.__marker = 1")
                pg.locator("nav.nav a[href='#ajuda']").first.click(); pg.wait_for_timeout(300)
                y1 = settle_scroll(pg)
                pg.go_back(); pg.wait_for_timeout(500)
                y0 = settle_scroll(pg)
                marker = pg.evaluate("window.__marker")
                assert marker == 1, "página recarregou"
                assert y0 < y1, {"before_back": y1, "after_back": y0}
                return {"y_at_anchor": y1, "y_after_back": y0}
            finally:
                c.close()

        # ---------- T08 carousels ----------
        ctx, page = new_page(browser, 1440, 900)
        page.wait_for_timeout(500)
        page.locator("#novidades").scroll_into_view_if_needed()
        page.wait_for_timeout(300)

        @run("T08a-carousel-desktop", "Carrossel Névoa 1440: 4 cartões inteiros, setas e bullets; anterior desabilitada na 1ª página")
        def _():
            info = page.evaluate("""() => { const c = document.querySelector('#novidades [data-carousel]'); const t = c.querySelector('.carousel__track');
              const tr = t.getBoundingClientRect(); const lis = [...t.children].filter(l=>!l.hidden);
              const full = lis.filter(l => { const r = l.getBoundingClientRect(); return r.left >= tr.left - 1 && r.right <= tr.right + 1; }).length;
              return {full, total: lis.length, navHidden: c.querySelector('.carousel__nav').hidden, dots: c.querySelectorAll('.dot').length,
                prevDisabled: c.querySelector('[data-dir="-1"]').getAttribute('aria-disabled'), nextDisabled: c.querySelector('[data-dir="1"]').getAttribute('aria-disabled')}; }""")
            assert info["full"] == 4 and not info["navHidden"] and info["dots"] >= 2 and info["prevDisabled"] == "true", info
            return info

        @run("T08b-carousel-arrows", "Carrossel Névoa 1440: seta próxima avança página, bullet atual muda; última página desabilita próxima; seta anterior volta")
        def _():
            c = "#novidades [data-carousel]"
            page.locator(f"{c} [data-dir='1']").click()
            settle_scroll(page, f"document.querySelector('{c} .carousel__track').scrollLeft")
            s1 = page.evaluate(f"""() => {{ const c = document.querySelector('{c}');
                return {{left: c.querySelector('.carousel__track').scrollLeft, current: [...c.querySelectorAll('.dot')].findIndex(d=>d.getAttribute('aria-current')==='true'),
                prev: c.querySelector('[data-dir="-1"]').getAttribute('aria-disabled'), next: c.querySelector('[data-dir="1"]').getAttribute('aria-disabled')}}; }}""")
            page.screenshot(path=str(SHOTS / "vitrine-pagina2-1440.png"))
            page.locator(f"{c} [data-dir='-1']").click()
            settle_scroll(page, f"document.querySelector('{c} .carousel__track').scrollLeft")
            s0 = page.evaluate(f"document.querySelector('{c} .carousel__track').scrollLeft")
            assert s1["left"] > 0 and s1["current"] == 1 and s1["prev"] == "false", s1
            assert s1["next"] == "true", f"com 8 peças / 4 por página a página 2 é a última: {s1}"
            assert s0 == 0, s0
            # bullet click
            page.locator(f"{c} .dot").nth(1).click()
            settle_scroll(page, f"document.querySelector('{c} .carousel__track').scrollLeft")
            s2 = page.evaluate(f"document.querySelector('{c} .carousel__track').scrollLeft")
            assert s2 > 0, "bullet não rolou"
            return {"after_next": s1, "after_prev": s0, "after_dot2": s2}

        @run("T08c-carousel-keyboard", "Carrossel 1440: trilho focável rola com ArrowRight (teclado)")
        def _():
            c = "#colecao-terra [data-carousel]"
            page.evaluate(f"document.querySelector('{c} .carousel__track').scrollLeft = 0")
            page.locator(f"{c} .carousel__track").focus()
            page.keyboard.press("ArrowRight"); page.wait_for_timeout(400)
            v = settle_scroll(page, f"document.querySelector('{c} .carousel__track').scrollLeft")
            assert v > 0, "ArrowRight não rolou o trilho"
            return {"scrollLeft": v}

        @run("T08d-carousel-past", "Carrosséis Terra/Sal 1440: 6 peças, 2 páginas, setas operam")
        def _():
            out = {}
            for sel in ["#colecao-terra", "#colecao-sal"]:
                c = f"{sel} [data-carousel]"
                page.evaluate(f"document.querySelector('{c} .carousel__track').scrollLeft = 0"); page.wait_for_timeout(200)
                page.locator(c).scroll_into_view_if_needed()
                page.locator(f"{c} [data-dir='1']").click()
                v = settle_scroll(page, f"document.querySelector('{c} .carousel__track').scrollLeft")
                dots = page.locator(f"{c} .dot").count()
                assert v > 0 and dots == 2, {sel: (v, dots)}
                out[sel] = {"scrollLeft": v, "dots": dots}
            return out
        ctx.close()

        ctx, page = new_page(browser, 375, 667)
        page.wait_for_timeout(400)

        @run("T08e-carousel-mobile", "Carrossel 375: sem setas, com bullets, 2 cartões + parte do 3º; rolagem por scroll atualiza bullet")
        def _():
            c = "#novidades [data-carousel]"
            page.locator(c).scroll_into_view_if_needed()
            info = page.evaluate(f"""() => {{ const c = document.querySelector('{c}'); const t = c.querySelector('.carousel__track');
              const vw = document.documentElement.clientWidth; const lis = [...t.children];
              const vis = lis.map(l => {{ const r = l.getBoundingClientRect(); return Math.max(0, Math.min(r.right, vw) - Math.max(r.left, 0)) / r.width; }});
              return {{navVisible: getComputedStyle(c.querySelector('.carousel__nav')).display !== 'none' && !c.querySelector('.carousel__nav').hidden,
                dots: c.querySelectorAll('.dot').length, dotsHidden: c.querySelector('.carousel__dots').hidden, visibleFractions: vis.slice(0,4).map(v=>+v.toFixed(2))}}; }}""")
            page.evaluate(f"(() => {{ const t = document.querySelector('{c} .carousel__track'); t.style.scrollBehavior='auto'; t.scrollLeft = t.scrollWidth; }})()")
            page.wait_for_timeout(400)
            last = page.evaluate(f"[...document.querySelectorAll('{c} .dot')].findIndex(d=>d.getAttribute('aria-current')==='true')")
            info["currentDotAtEnd"] = last
            page.screenshot(path=str(SHOTS / "vitrine-375.png"))
            fr = info["visibleFractions"]
            assert not info["navVisible"] and info["dots"] >= 2 and not info["dotsHidden"], info
            assert fr[0] > 0.99 and fr[1] > 0.99 and 0.1 < fr[2] < 0.9, info
            assert last == info["dots"] - 1, info
            return info
        ctx.close()

        # ---------- T09 bag ----------
        for (w, h) in [(375, 667), (1440, 900)]:
            ctx, page = new_page(browser, w, h)
            page.wait_for_timeout(300)

            @run(f"T09a-bag-add-{w}", f"Sacola {w}: adicionar atualiza contador, toast e subtotal")
            def _(w=w):
                b1 = page.locator("[data-add='nevoa-caneca']")
                b1.scroll_into_view_if_needed(); b1.click()
                page.wait_for_timeout(200)
                count = page.locator("[data-cart-count]").first.inner_text()
                toast = page.locator("[data-toast]").inner_text()
                btn_txt = b1.inner_text()
                page.locator("[data-add='nevoa-jarra']").scroll_into_view_if_needed()
                page.locator("[data-add='nevoa-jarra']").click(); page.wait_for_timeout(200)
                count2 = page.locator("[data-cart-count]").first.inner_text()
                sub = page.evaluate("document.querySelector('[data-cart-subtotal]').textContent")
                bag_label = page.evaluate("(() => { const b = document.querySelector('.bag-btn'); return (b.getAttribute('aria-label') || b.innerText).trim(); })()")
                assert count == "1" and count2 == "2", (count, count2)
                assert "Caneca Névoa" in toast, toast
                assert sub == "R$ 266", sub
                return {"count": count2, "toast": toast, "btn_after": btn_txt, "subtotal": sub, "bag_name": bag_label}

            @run(f"T09b-bag-drawer-{w}", f"Sacola {w}: abre, foco no painel, +/−, remover, total, frete, finalizar, Esc devolve foco")
            def _(w=w):
                bag = page.locator(".bag-btn").first
                page.evaluate("window.scrollTo(0,0)")
                bag.click(); page.wait_for_timeout(450)
                assert page.locator("#sacola").is_visible()
                assert bag.get_attribute("aria-expanded") == "true"
                assert page.evaluate("!!document.activeElement.closest('#sacola .drawer__panel')")
                items = page.locator(".cart__item").count()
                page.screenshot(path=str(SHOTS / f"sacola-{w}.png"))
                page.get_by_role("button", name="Aumentar quantidade de Caneca Névoa").click(); page.wait_for_timeout(100)
                q = page.locator(".cart__item[data-id='nevoa-caneca'] output").inner_text()
                sub = page.locator("[data-cart-subtotal]").inner_text()
                focus_after_plus = page.evaluate("document.activeElement.getAttribute('aria-label')")
                ship = page.locator("[data-ship-text]").inner_text()
                page.get_by_role("button", name="Diminuir quantidade de Caneca Névoa").click(); page.wait_for_timeout(100)
                q2 = page.locator(".cart__item[data-id='nevoa-caneca'] output").inner_text()
                page.get_by_role("button", name="Remover Jarra Névoa").click(); page.wait_for_timeout(100)
                sub2 = page.locator("[data-cart-subtotal]").inner_text()
                count = page.locator("[data-cart-count]").first.inner_text()
                page.get_by_role("button", name="Finalizar compra").click(); page.wait_for_timeout(100)
                notice = page.locator("[data-checkout-notice]").inner_text()
                notice_live = page.evaluate("(() => { const n = document.querySelector('[data-checkout-notice]'); return n.getAttribute('role') || n.getAttribute('aria-live'); })()")
                page.keyboard.press("Escape"); page.wait_for_timeout(450)
                closed = page.evaluate("document.querySelector('#sacola').hidden")
                back = page.evaluate("document.activeElement.classList.contains('bag-btn')")
                res = {"items": items, "qty_after_plus": q, "subtotal_after_plus": sub, "focus_after_plus": focus_after_plus, "ship": ship,
                       "qty_after_minus": q2, "subtotal_after_remove": sub2, "count": count, "notice": notice, "notice_live": notice_live,
                       "closed": closed, "focus_back": back}
                assert items == 2 and q == "2" and sub == "R$ 364" and q2 == "1" and sub2 == "R$ 98" and count == "1", res
                assert "demonstrativa" in notice and closed and back, res
                return res

            @run(f"T09c-bag-persist-empty-{w}", f"Sacola {w}: persiste após recarregar; − até zero esvazia e mostra estado vazio")
            def _(w=w):
                page.reload(); page.wait_for_load_state("load"); page.wait_for_timeout(300)
                count = page.locator("[data-cart-count]").first.inner_text()
                page.locator(".bag-btn").first.click(); page.wait_for_timeout(450)
                page.get_by_role("button", name="Diminuir quantidade de Caneca Névoa").click(); page.wait_for_timeout(150)
                empty = page.locator("[data-cart-empty]").is_visible()
                foot = page.locator("[data-cart-foot]").is_visible()
                focus = page.evaluate("document.activeElement.getAttribute('aria-label')")
                count2 = page.locator("[data-cart-count]").first.inner_text()
                page.screenshot(path=str(SHOTS / f"sacola-vazia-{w}.png"))
                page.get_by_role("button", name="Fechar sacola").click(); page.wait_for_timeout(450)
                res = {"count_after_reload": count, "empty_visible": empty, "foot_visible": foot, "focus_after_empty": focus, "count": count2}
                assert count == "1" and empty and not foot and count2 == "0", res
                return res

            @run(f"T09d-bag-trap-{w}", f"Sacola {w}: foco preso no painel (20 Tabs) e fundo inert")
            def _(w=w):
                page.locator("[data-add='sal-prato']").scroll_into_view_if_needed()
                page.locator("[data-add='sal-prato']").click()
                page.evaluate("window.scrollTo(0,0)")
                page.locator(".bag-btn").first.click(); page.wait_for_timeout(450)
                esc = []
                for i in range(20):
                    page.keyboard.press("Tab")
                    if not page.evaluate("!!document.activeElement.closest('#sacola .drawer__panel')"):
                        esc.append(i)
                inert = page.evaluate("document.querySelector('#conteudo').hasAttribute('inert')")
                page.keyboard.press("Escape"); page.wait_for_timeout(450)
                assert not esc and inert, {"escaped": esc, "inert": inert}
            ctx.close()

        @run("T09e-bag-tamper", "Sacola: localStorage adulterado (id inexistente, qty absurda, preço) é saneado")
        def _():
            c, pg = new_page(browser, 375, 667)
            try:
                pg.evaluate("""localStorage.setItem('bruma-sacola-v1', JSON.stringify([{id:'nevoa-caneca', qty: 999, price: 1}, {id:'<img src=x onerror=alert(1)>', qty:1}, {id:'sal-prato', qty:-3}, 'lixo']))""")
                pg.reload(); pg.wait_for_load_state("load"); pg.wait_for_timeout(300)
                count = pg.locator("[data-cart-count]").first.inner_text()
                sub = pg.evaluate("document.querySelector('[data-cart-subtotal]').textContent")
                assert count == "20" and sub == "R$ 1.960", (count, sub)
                return {"count": count, "subtotal": sub}
            finally:
                c.close()

        # ---------- T10 keyboard navigation & visible focus ----------
        for (w, h) in [(375, 667), (1440, 900)]:
            ctx, page = new_page(browser, w, h, motion="reduce")
            page.wait_for_timeout(300)

            @run(f"T10a-skip-{w}", f"Teclado {w}: 1º Tab = 'Pular para o conteúdo' visível; Enter foca main")
            def _(w=w):
                page.keyboard.press("Tab")
                f = page.evaluate(FOCUS_VISIBLE_JS)
                page.screenshot(path=str(SHOTS / f"skip-link-{w}.png"))
                page.keyboard.press("Enter"); page.wait_for_timeout(200)
                main_focus = page.evaluate("document.activeElement.id")
                assert "Pular" in f["text"] and f["inViewport"] and f["visibleIndicator"], f
                assert main_focus == "conteudo", main_focus
                return {"first": f, "after_enter": main_focus}

            @run(f"T10b-tab-walk-{w}", f"Teclado {w}: percorrer 120 Tabs; todo foco tem indicador visível e não fica sob o header")
            def _(w=w):
                page.evaluate("window.scrollTo(0,0)"); page.evaluate("document.activeElement && document.activeElement.blur()")
                page.keyboard.press("Tab")
                seen, no_ind, obscured, partly = [], [], [], []
                for i in range(120):
                    f = page.evaluate(FOCUS_VISIBLE_JS)
                    if f is None:
                        break
                    seen.append(f"{f['tag']}:{f['text'][:24]}")
                    if not f["visibleIndicator"]:
                        no_ind.append(f)
                    if f["obscuredByHeader"]:
                        obscured.append(f)
                    elif f["partlyUnderHeader"]:
                        partly.append(f)
                    page.keyboard.press("Tab")
                    page.wait_for_timeout(30)
                res = {"steps": len(seen), "without_indicator": no_ind[:10], "fully_obscured_by_header": obscured[:10],
                       "partly_under_header": partly[:10], "sequence_head": seen[:30]}
                assert not no_ind and not obscured, res
                return res

            @run(f"T10c-details-{w}", f"Teclado {w}: acordeão de Ajuda abre com Enter/Espaço")
            def _(w=w):
                s = page.locator("#envio summary")
                s.focus(); page.keyboard.press("Enter"); page.wait_for_timeout(100)
                o1 = page.evaluate("document.querySelector('#envio').open")
                page.keyboard.press("Space"); page.wait_for_timeout(100)
                o2 = page.evaluate("document.querySelector('#envio').open")
                assert o1 and not o2, (o1, o2)
            ctx.close()

        # ---------- T11 no-JS ----------
        for (w, h) in [(375, 667), (1440, 900)]:
            ctx, page = new_page(browser, w, h, js=False)
            page.wait_for_timeout(300)

            @run(f"T11-nojs-{w}", f"Sem JavaScript {w}: nav visível, vitrines rolam, controles JS ocultos, sem overflow, âncoras funcionam")
            def _(w=w):
                info = page.evaluate("""() => { const vis = el => !!el && getComputedStyle(el).display !== 'none' && el.getBoundingClientRect().width > 0;
                  const tracks = [...document.querySelectorAll('.carousel__track')].map(t => ({sw: t.scrollWidth, cw: t.clientWidth, ox: getComputedStyle(t).overflowX}));
                  return {noJsClass: document.documentElement.classList.contains('no-js'), navVisible: vis(document.querySelector('nav.nav')),
                   hamburgerVisible: vis(document.querySelector('.header__menu')), bagVisible: vis(document.querySelector('.bag-btn')),
                   addVisible: [...document.querySelectorAll('.add')].some(vis), tracks,
                   pricesVisible: [...document.querySelectorAll('.card')].length,
                   scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth,
                   arrowsVisible: [...document.querySelectorAll('.carousel__nav')].some(vis), filterLinks: document.querySelectorAll('a[data-filter]').length}; }""")
                page.screenshot(path=str(SHOTS / f"sem-js-{w}-full.png"), full_page=True)
                page.locator("nav.nav a[href='#ajuda']").first.click(); page.wait_for_timeout(300)
                info["hash_after_click"] = page.evaluate("location.hash")
                info["ajuda_top"] = page.evaluate("document.querySelector('#t-ajuda').getBoundingClientRect().top")
                # skip link
                page.evaluate("window.scrollTo(0,0)")
                page.keyboard.press("Tab")
                info["first_tab"] = page.evaluate("document.activeElement.textContent.trim()")
                ok = (info["noJsClass"] and info["navVisible"] and not info["hamburgerVisible"] and not info["bagVisible"]
                      and not info["addVisible"] and all(t["ox"] in ("auto", "scroll") and t["sw"] > t["cw"] for t in info["tracks"])
                      and info["scrollWidth"] <= info["clientWidth"] and info["hash_after_click"] == "#ajuda")
                assert ok, info
                return info
            ctx.close()

        @run("T11b-nojs-filter-links", "Sem JavaScript: links de categoria/momento levam a uma âncora válida (filtro indisponível)")
        def _():
            c, pg = new_page(browser, 375, 667, js=False)
            try:
                hrefs = pg.evaluate("[...new Set([...document.querySelectorAll('a[data-filter]')].map(a=>a.getAttribute('href')))]")
                missing = [h for h in hrefs if not pg.evaluate(f"!!document.getElementById('{h[1:]}')")]
                assert not missing, missing
                return {"hrefs": hrefs}
            finally:
                c.close()

        # ---------- T12 reduced motion ----------
        @run("T12-reduced-motion", "prefers-reduced-motion: nenhuma animação CSS rodando; scroll-behavior auto; transições ~0")
        def _():
            out = {}
            for motion in ["no-preference", "reduce"]:
                c, pg = new_page(browser, 1440, 900, motion=motion)
                pg.wait_for_timeout(800)
                out[motion] = pg.evaluate("""() => { const anims = document.getAnimations().filter(a => a.playState === 'running');
                  const drawerT = getComputedStyle(document.querySelector('.drawer__panel')).transitionDuration;
                  return {running: anims.length, names: [...new Set(anims.map(a => a.animationName || a.transitionProperty || 'anim'))].slice(0,8),
                   scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior, drawerTransition: drawerT}; }""")
                pg.locator(".bag-btn").first.click(); pg.wait_for_timeout(50)
                out[motion]["running_after_open_bag"] = pg.evaluate("document.getAnimations().filter(a => a.playState === 'running').length")
                c.close()
            r = out["reduce"]
            assert r["running"] == 0 and r["scrollBehavior"] == "auto" and r["running_after_open_bag"] == 0, out
            return out

        # ---------- T13 image weight above the fold + CLS/LCP lab ----------
        for (w, h) in [(375, 667), (1440, 900)]:
            @run(f"T13-weight-cls-{w}", f"Peso de imagens carregadas sem rolar (site/assets/fotos) e CLS/LCP de laboratório ({w}px, sem throttling)")
            def _(w=w, h=h):
                c = browser.new_context(viewport={"width": w, "height": h})
                pg = c.new_page()
                pg.add_init_script("""window.__cls = 0; window.__lcp = null; window.__shifts = [];
                  new PerformanceObserver(l => l.getEntries().forEach(e => { if (!e.hadRecentInput) { window.__cls += e.value; window.__shifts.push({v: e.value, src: (e.sources||[]).map(s => s.node && (s.node.className || s.node.nodeName)).slice(0,3)}); } })).observe({type: 'layout-shift', buffered: true});
                  new PerformanceObserver(l => { const e = l.getEntries().pop(); window.__lcp = {t: e.startTime, el: e.element && (e.element.currentSrc || e.element.className || e.element.nodeName), size: e.size}; }).observe({type: 'largest-contentful-paint', buffered: true});""")
                pg.goto(URL); pg.wait_for_load_state("load"); pg.wait_for_timeout(1200)
                names = pg.evaluate("performance.getEntriesByType('resource').map(r => r.name)")
                fotos = sorted({n for n in names if "/assets/fotos/" in n})
                files = []
                for n in fotos:
                    rel = n.split("/assets/", 1)[1]; rel = "assets/" + rel
                    files.append({"file": rel, "bytes": os.path.getsize(ROOT / "site" / rel)})
                total_all = sum(os.path.getsize(ROOT / "site" / n.split(BASE, 1)[1]) for n in names if n.startswith(BASE) and os.path.exists(ROOT / "site" / n.split(BASE, 1)[1]))
                cls_load = pg.evaluate("window.__cls")
                lcp = pg.evaluate("window.__lcp")
                scroll_through(pg)
                cls_scroll = pg.evaluate("window.__cls")
                shifts = pg.evaluate("window.__shifts")
                imgs_no_dims = pg.evaluate("[...document.images].filter(i => !i.getAttribute('width') || !i.getAttribute('height')).map(i => i.src)")
                c.close()
                res = {"fotos_loaded_without_scroll": files, "fotos_bytes": sum(f["bytes"] for f in files),
                       "all_local_resources_bytes": total_all, "cls_after_load": round(cls_load, 4),
                       "cls_after_full_scroll": round(cls_scroll, 4), "shifts": shifts[:8], "lcp_ms_lab_unthrottled": lcp,
                       "imgs_without_width_height": imgs_no_dims}
                assert not imgs_no_dims and cls_scroll <= 0.1, res
                return res

        # ---------- T14 static a11y / structure checks (in-page JS, offline) ----------
        ctx, page = new_page(browser, 1440, 900)
        page.wait_for_timeout(300)

        @run("T14a-structure", "Estrutura: 1 h1, sem salto de nível de heading, landmarks, ids únicos, alt em todas as imagens, nome em todos os botões")
        def _():
            info = page.evaluate("""() => {
              const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(h => !h.closest('[hidden]'));
              const seq = hs.map(h => +h.tagName[1]); const jumps = [];
              for (let i = 1; i < seq.length; i++) if (seq[i] - seq[i-1] > 1) jumps.push({from: hs[i-1].textContent.trim().slice(0,30), to: hs[i].textContent.trim().slice(0,30), levels: [seq[i-1], seq[i]]});
              const ids = [...document.querySelectorAll('[id]')].map(e => e.id); const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
              const noAlt = [...document.images].filter(i => !i.hasAttribute('alt')).map(i => i.src);
              const btnNoName = [...document.querySelectorAll('button')].filter(b => !(b.getAttribute('aria-label') || b.textContent.trim() || b.getAttribute('aria-labelledby'))).map(b => b.outerHTML.slice(0,80));
              const altList = [...document.images].map(i => ({src: i.getAttribute('src').split('/').pop(), alt: i.alt}));
              return {h1: seq.filter(x => x === 1).length, headings: hs.map(h => h.tagName + ' ' + h.textContent.trim().slice(0, 40)), jumps, dupIds: dup, noAlt, btnNoName,
                landmarks: {main: document.querySelectorAll('main').length, header: !!document.querySelector('body > header, [data-header]'), footer: !!document.querySelector('footer'), navs: [...document.querySelectorAll('nav')].map(n => n.getAttribute('aria-label'))},
                lang: document.documentElement.lang, title: document.title, altList, emptyAlt: altList.filter(a => a.alt === '').length,
                metaDesc: !!document.querySelector('meta[name=description]')};
            }""")
            ok = info["h1"] == 1 and not info["jumps"] and not info["dupIds"] and not info["noAlt"] and not info["btnNoName"] and info["landmarks"]["main"] == 1 and info["lang"] == "pt-BR"
            assert ok, info
            return info

        @run("T14b-targets-375", "Alvos de toque ≥ 24×24 px em 375 (WCAG 2.5.8), sem considerar exceções de espaçamento")
        def _():
            c, pg = new_page(browser, 375, 667)
            try:
                small = pg.evaluate("""() => [...document.querySelectorAll('a[href], button, summary, [tabindex="0"]')].filter(e => {
                    if (e.closest('[hidden]')) return false; const r = e.getBoundingClientRect(); if (!r.width) return false;
                    const inline = getComputedStyle(e).display === 'inline' && e.closest('p, li, dd');
                    return !inline && (r.width < 24 || r.height < 24); }).map(e => ({tag: e.tagName, text: (e.getAttribute('aria-label') || e.textContent).trim().slice(0, 30), w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height)}))""")
                assert not small, small
            finally:
                c.close()

        @run("T14c-forbidden", "Conteúdo proibido: sem <form>, wa.me/WhatsApp, tel:, scripts externos, depoimento/avaliação/estrelas/mais vendido, contato/encomenda (AC-ECOM-07)")
        def _():
            html = (ROOT / "site" / "index.html").read_text(encoding="utf-8").lower()
            # "piloto de avaliação" no aviso do rodapé é o disclaimer da marca fictícia, não avaliação de cliente: removido antes da busca
            text = page.evaluate("document.body.innerText").lower().replace("piloto de avaliação", "piloto de [disclaimer]")
            pats = {"<form": html, "wa.me": html, "whatsapp": html, "tel:": html, "src=\"http": html, "href=\"http": html,
                    "depoimento": text, "avaliaç": text, "nota ": text, "★": text, "estrelas": text, "mais vendido": text, "encomenda": text, "id=\"contato\"": html, "últimas peças": text}
            found = {k: src.count(k) for k, src in pats.items() if k in src}
            assert not found, found
        ctx.close()

        # ---------- T15 axe-core ----------
        if AXE and AXE.exists():
            axe_src = AXE.read_text(encoding="utf-8")
            axe_all = {}
            states = [(w, h, None) for (w, h) in [(320, 568), (375, 667), (768, 1024), (1024, 768), (1440, 900)]] + [(375, 667, "menu"), (375, 667, "sacola"), (1440, 900, "sacola"), (375, 667, "filtro")]
            for (w, h, state) in states:
                key = f"{w}" + (f"-{state}" if state else "")
                c, pg = new_page(browser, w, h, motion="reduce")
                scroll_through(pg)
                if state == "menu":
                    pg.get_by_role("button", name="Abrir menu").click(); pg.wait_for_timeout(400)
                elif state == "sacola":
                    pg.locator("[data-add='nevoa-caneca']").scroll_into_view_if_needed(); pg.locator("[data-add='nevoa-caneca']").click()
                    pg.evaluate("window.scrollTo(0,0)"); pg.locator(".bag-btn").first.click(); pg.wait_for_timeout(400)
                elif state == "filtro":
                    pg.locator("a.cat").first.click(); pg.wait_for_timeout(400)
                pg.add_script_tag(content=axe_src)
                r = pg.evaluate("""async () => { const r = await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}, resultTypes: ['violations','incomplete']});
                    const m = v => ({id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.slice(0,6).map(n => ({target: n.target.join(' '), summary: (n.failureSummary||'').slice(0,240)})), count: v.nodes.length});
                    return {version: axe.version, violations: r.violations.map(m), incomplete: r.incomplete.map(m), passes: r.passes.length}; }""")
                axe_all[key] = r
                c.close()
            (OUT / f"axe-results-{TAG}.json").write_text(json.dumps(axe_all, ensure_ascii=False, indent=1), encoding="utf-8")
            for key, r in axe_all.items():
                @run(f"T15-axe-{key}", f"axe-core {r['version']} ({key}): 0 violações critical/serious")
                def _(r=r):
                    sev = [v for v in r["violations"] if v["impact"] in ("critical", "serious")]
                    other = [{"id": v["id"], "impact": v["impact"], "count": v["count"]} for v in r["violations"] if v["impact"] not in ("critical", "serious")]
                    inc = [{"id": v["id"], "count": v["count"]} for v in r["incomplete"]]
                    assert not sev, {"serious_or_critical": sev, "other": other}
                    return {"other_violations": other, "incomplete": inc, "passes": r["passes"]}
        else:
            record("T15-axe", "axe-core", "NOT_RUN", {"reason": "axe.min.js não fornecido"})

        # ---------- T16 contraste calculado (fundo sólido do ancestral; texto sobre foto por amostragem de pixels) ----------
        CONTRAST_JS = """() => {
          const lum = c => { const [r,g,b] = c.map(v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); }); return 0.2126*r + 0.7152*g + 0.0722*b; };
          const parse = s => { const m = s.match(/rgba?\\(([^)]+)\\)/); if (!m) return null; const p = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return {rgb: p.slice(0,3), a: p.length > 3 ? p[3] : 1}; };
          const ratio = (a, b) => { const L1 = lum(a), L2 = lum(b); return (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05); };
          const bgOf = el => { let stack = []; for (let e = el; e; e = e.parentElement) { const cs = getComputedStyle(e);
              if (cs.backgroundImage !== 'none' && !cs.backgroundImage.startsWith('linear-gradient') && e !== document.documentElement) return {image: true, el: e.className};
              const c = parse(cs.backgroundColor); if (c && c.a > 0) { stack.push(c); if (c.a >= 1) break; } }
            let base = [255,255,255]; for (let i = stack.length - 1; i >= 0; i--) { const c = stack[i]; base = base.map((v, k) => c.rgb[k]*c.a + v*(1-c.a)); } return {rgb: base}; };
          const out = []; const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          const seen = new Set();
          while (walker.nextNode()) { const t = walker.currentNode; if (!t.textContent.trim()) continue; const el = t.parentElement; if (seen.has(el)) continue; seen.add(el);
            if (el.closest('[hidden], [aria-hidden="true"], .sr-only, .skip, [data-drawer]')) continue;
            const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue; const cs = getComputedStyle(el);
            if (cs.visibility === 'hidden' || +cs.opacity === 0) continue;
            const fg = parse(cs.color); const bg = bgOf(el); const size = parseFloat(cs.fontSize), w = +cs.fontWeight;
            const large = size >= 24 || (size >= 18.66 && w >= 700);
            const inHero = !!el.closest('.hero');
            if (bg.image || inHero) { out.push({text: t.textContent.trim().slice(0,40), cls: el.className, overImage: true, fg: fg.rgb, large}); continue; }
            const rr = ratio(fg.rgb, bg.rgb); out.push({text: t.textContent.trim().slice(0,40), cls: typeof el.className === 'string' ? el.className : '', ratio: +rr.toFixed(2), large, need: large ? 3 : 4.5, fg: fg.rgb.map(Math.round), bg: bg.rgb.map(Math.round)}); }
          return out; }"""
        for (w, h) in [(375, 667), (1440, 900)]:
            @run(f"T16-contrast-{w}", f"Contraste de texto calculado (WCAG 1.4.3) em {w}px; texto sobre a foto do banner por amostragem de pixels")
            def _(w=w, h=h):
                from PIL import Image
                import io
                c, pg = new_page(browser, w, h, motion="reduce")
                try:
                    pg.wait_for_timeout(600)
                    rows = pg.evaluate(CONTRAST_JS)
                    solid = [r for r in rows if not r.get("overImage")]
                    fails = [r for r in solid if r["ratio"] < r["need"]]
                    # banner: oculta o texto, fotografa a área de cada elemento e mede o pior pixel contra a cor do texto
                    hero = []
                    els = pg.evaluate("""() => [...document.querySelectorAll('.hero .tag, .hero h1, .hero h1 em, .hero__lead, .hero .btn, .hero .btn-link, .hero__pause')].filter(e => e.getBoundingClientRect().width).map((e, i) => { e.dataset.qaC = i; const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return {i, cls: e.className, text: e.textContent.trim().slice(0,30), x: r.x, y: r.y + scrollY, w: r.width, h: r.height, fg: cs.color, bg: cs.backgroundColor, size: parseFloat(cs.fontSize), weight: +cs.fontWeight}; })""")
                    pg.add_style_tag(content=".hero [data-qa-c], .hero [data-qa-c] * { color: transparent !important; text-shadow: none !important; }")
                    pg.wait_for_timeout(200)
                    shot = Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert("RGB")
                    def lum(c):
                        def ch(v):
                            v /= 255
                            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
                        r_, g_, b_ = (ch(x) for x in c)
                        return 0.2126 * r_ + 0.7152 * g_ + 0.0722 * b_
                    import re as _re
                    for e in els:
                        fg = [float(x) for x in _re.findall(r"[\d.]+", e["fg"])[:3]]
                        box = shot.crop((int(e["x"]), int(e["y"]), int(e["x"] + e["w"]), int(e["y"] + e["h"])))
                        px = list(box.getdata())[::7] or [(255, 255, 255)]
                        Lf = lum(fg)
                        ratios = sorted(((max(Lf, lum(p)) + 0.05) / (min(Lf, lum(p)) + 0.05)) for p in px)
                        worst, p10 = ratios[0], ratios[len(ratios) // 10]
                        large = e["size"] >= 24 or (e["size"] >= 18.66 and e["weight"] >= 700)
                        hero.append({"el": e["cls"] or e["text"], "text": e["text"], "fg": e["fg"], "own_bg": e["bg"], "worst_pixel_ratio": round(worst, 2), "p10_ratio": round(p10, 2), "need": 3 if large else 4.5})
                    hero_fails = [x for x in hero if x["p10_ratio"] < x["need"]]
                    res = {"checked_solid": len(solid), "solid_fails": fails, "hero": hero, "hero_fails_p10": hero_fails,
                           "min_solid": min(solid, key=lambda r: r["ratio"]) if solid else None}
                    assert not fails and not hero_fails, res
                    return res
                finally:
                    c.close()

        # ---------- T17 ordem de Tab completa a partir do topo (página nova) ----------
        for (w, h) in [(375, 667), (1440, 900)]:
            @run(f"T17-tab-from-top-{w}", f"Tab desde o carregamento ({w}px): header, conteúdo e rodapé alcançáveis; foco visível em todos")
            def _(w=w, h=h):
                c, pg = new_page(browser, w, h, motion="reduce")
                try:
                    pg.wait_for_timeout(300)
                    seq, noind, obsc = [], [], []
                    for i in range(140):
                        pg.keyboard.press("Tab"); pg.wait_for_timeout(20)
                        f = pg.evaluate(FOCUS_VISIBLE_JS)
                        if f is None:
                            break
                        where = pg.evaluate("(() => { const e = document.activeElement; return e.closest('[data-header]') ? 'header' : e.closest('footer') ? 'footer' : e.closest('main') ? 'main' : e.closest('.announce') ? 'announce' : 'other'; })()")
                        seq.append(f"{where}:{f['tag']}:{f['text'][:22]}")
                        if not f["visibleIndicator"]:
                            noind.append(f)
                        if (f["obscuredByHeader"] or f["partlyUnderHeader"]) and not f["text"].startswith("Pular"):
                            obsc.append(f)
                        if len(seq) > 3 and seq[-1] == seq[0]:
                            break
                    regions = sorted(set(x.split(":")[0] for x in seq))
                    res = {"steps": len(seq), "regions": regions, "sequence": seq, "no_indicator": noind,
                           "fully_under_header_2_4_11": [o for o in obsc if o["obscuredByHeader"]], "partly_under_header_2_4_12": [o for o in obsc if not o["obscuredByHeader"]]}
                    assert "header" in regions and "footer" in regions and not noind and not res["fully_under_header_2_4_11"], res
                    return res
                finally:
                    c.close()

        # ---------- T18 gavetas abertas pelo teclado: foco visível no 1º elemento ----------
        @run("T18-drawer-keyboard-focus", "Menu e sacola abertos com Enter (375): 1º foco no painel tem indicador visível")
        def _():
            c, pg = new_page(browser, 375, 667, motion="reduce")
            try:
                out = {}
                pg.get_by_role("button", name="Abrir menu").focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
                out["menu"] = pg.evaluate(FOCUS_VISIBLE_JS)
                pg.screenshot(path=str(SHOTS / "menu-teclado-375.png"))
                pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                pg.locator(".bag-btn").first.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
                out["bag"] = pg.evaluate(FOCUS_VISIBLE_JS)
                pg.screenshot(path=str(SHOTS / "sacola-teclado-375.png"))
                assert out["menu"]["visibleIndicator"] and out["bag"]["visibleIndicator"], out
                return out
            finally:
                c.close()

        # ---------- T19 nomes acessíveis (árvore de acessibilidade do Chromium) ----------
        @run("T19-accessible-names", "Nomes acessíveis: sacola, adicionar, setas, bullets, hambúrguer (aria snapshot do Chromium)")
        def _():
            c, pg = new_page(browser, 1440, 900)
            try:
                pg.locator("[data-add='nevoa-caneca']").click(); pg.wait_for_timeout(100)
                snap = {"header": pg.locator("[data-header]").aria_snapshot(),
                        "first_card": pg.locator("#novidades .carousel__track > li").first.aria_snapshot(),
                        "carousel_controls": pg.locator("#novidades .carousel__nav").aria_snapshot(),
                        "dots": pg.locator("#novidades .carousel__dots").aria_snapshot(),
                        "sold_out": pg.locator(".carousel__track > li:has(button.add[disabled])").first.aria_snapshot()}
                (OUT / f"aria-snapshot-{TAG}.yml").write_text("\n\n".join(f"# {k}\n{v}" for k, v in snap.items()), encoding="utf-8")
                bag_name = pg.get_by_role("button", name=re.compile("Sacola")).first.evaluate("e => e.textContent.replace(/\\s+/g,' ').trim()")
                # Reteste afbd689: nomes "Adicionar à sacola: <peça>" / "Adicionada à sacola: <peça>" (1,6 s) / "Esgotado: <peça>" (Quality P2-3, WCAG 2.5.3)
                names = {"done_after_click": pg.get_by_role("button", name="Adicionada à sacola: Caneca Névoa", exact=True).count()}
                pg.wait_for_timeout(1900)
                names["add_after_1_9s"] = pg.get_by_role("button", name="Adicionar à sacola: Caneca Névoa", exact=True).count()
                names["add_all"] = pg.get_by_role("button", name=re.compile(r"^Adicionar à sacola: .+")).count()
                names["sold_out"] = pg.locator("button.add[disabled]").evaluate_all("bs => bs.map(b => b.getAttribute('aria-label'))")
                names["sold_out_role_ok"] = pg.get_by_role("button", name="Esgotado: Prato raso Terra Molhada", exact=True).count()
                names["old_name"] = pg.get_by_role("button", name="Adicionar Caneca Névoa à sacola", exact=True).count()
                names["label_in_name"] = pg.locator("[data-add]").evaluate_all("bs => bs.every(b => b.getAttribute('aria-label').startsWith(b.querySelector('.add__long').textContent.trim()) || b.getAttribute('aria-label').startsWith(b.querySelector('.add__short').textContent.trim()))")
                assert names["done_after_click"] == 1 and names["add_after_1_9s"] == 1 and names["sold_out_role_ok"] == 1 and names["old_name"] == 0 \
                    and all(re.match(r"^Esgotado: .+", n or "") for n in names["sold_out"]) and names["label_in_name"], {"names": names, "snap": snap}
                return {"bag_text": bag_name, "names": names, "snapshots_file": f"aria-snapshot-{TAG}.yml", "header": snap["header"][:600], "sold_out": snap["sold_out"][:400]}
            finally:
                c.close()

        # ---------- T20 paisagem 667x375 e primeira tela ----------
        @run("T20-landscape", "Paisagem 667×375: sem rolagem horizontal; header não ocupa a tela")
        def _():
            c, pg = new_page(browser, 667, 375)
            try:
                scroll_through(pg)
                o = pg.evaluate(OVERFLOW_JS)
                o["header_h"] = pg.evaluate("document.querySelector('[data-header]').getBoundingClientRect().height")
                pg.screenshot(path=str(SHOTS / "paisagem-667x375.png"))
                assert o["scrollWidth"] <= o["clientWidth"] and o["header_h"] < 375 * 0.4, o
                return o
            finally:
                c.close()

        # Decisão do proprietário (2026-10-22, BUG-01 "foto mais baixa no celular"): escopo = CTA sem rolar em 375×667 e maiores.
        # 320×568 e 360×640 ficam fora da decisão: CTA abaixo da dobra é registrado como KNOWN_P3 (não P1); o resto do critério continua exigido.
        OUT_OF_SCOPE_FOLD = {320, 360}
        for (w, h) in [(320, 568), (360, 640), (375, 667), (390, 844), (414, 896)]:
            @run(f"T21-first-screen-{w}", f"Primeira tela {w}×{h}: h1 e CTA 'Comprar a coleção' visíveis sem rolar; CTA leva a #novidades com título visível"
                 + (" [CTA na dobra fora do escopo da decisão de 2026-10-22]" if w in OUT_OF_SCOPE_FOLD else ""))
            def _(w=w, h=h):
                c, pg = new_page(browser, w, h, motion="reduce")
                try:
                    pg.wait_for_timeout(400)
                    info = pg.evaluate("""() => { const r = s => { const e = document.querySelector(s); const b = e.getBoundingClientRect(); return {top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
                        return {h1: r('#t-hero'), cta: r('.hero .btn'), vh: innerHeight, cta_text: document.querySelector('.hero .btn').textContent.trim()}; }""")
                    pg.screenshot(path=str(SHOTS / f"primeira-tela-{w}.png"))
                    pg.locator(".hero .btn").click(); pg.wait_for_timeout(300)
                    info["hash"] = pg.evaluate("location.hash")
                    info["title_top"] = pg.evaluate("document.querySelector('#t-novidades').getBoundingClientRect().top")
                    info["hb"] = pg.evaluate("document.querySelector('[data-header]').getBoundingClientRect().bottom")
                    pg.keyboard.press("Tab")
                    info["tab_after_cta"] = pg.evaluate("(() => { const e = document.activeElement; return (e.getAttribute('aria-label') || e.textContent).trim().replace(/\\s+/g,' ').slice(0,40) + ' @' + (e.closest('section') || {}).id; })()")
                    rest_ok = info["h1"]["bottom"] <= h and info["hash"] == "#novidades" and info["hb"] <= info["title_top"] < h
                    cta_ok = info["cta"]["bottom"] <= h
                    if w in OUT_OF_SCOPE_FOLD and rest_ok and not cta_ok:
                        info["known_issue"] = {"severity": "P3", "why": "CTA abaixo da dobra; fora do escopo da decisão do proprietário de 2026-10-22 (375×667+)", "px_below_fold": info["cta"]["bottom"] - h}
                        return ("KNOWN_P3", info)
                    assert rest_ok and cta_ok, info
                    return info
                finally:
                    c.close()

        # ---------- T22 no-JS: âncora rola até o alvo ----------
        @run("T22-nojs-anchor-scroll", "Sem JavaScript (375): clicar 'Ajuda' leva o título para baixo do header (após a rolagem suave)")
        def _():
            c, pg = new_page(browser, 375, 667, js=False)
            try:
                pg.locator("nav.nav a[href='#ajuda']").first.click()
                pg.wait_for_timeout(300)
                settle_scroll(pg, timeout=5000)
                top = pg.evaluate("document.querySelector('#t-ajuda').getBoundingClientRect().top")
                hb = pg.evaluate("document.querySelector('[data-header]').getBoundingClientRect().bottom")
                pg.screenshot(path=str(SHOTS / "sem-js-ajuda-375.png"))
                assert hb - 1 <= top < 667, {"top": top, "header_bottom": hb}
                return {"top": top, "header_bottom": hb}
            finally:
                c.close()

        # ---------- T23 imagens bloqueadas (AC-CON-05) ----------
        @run("T23-images-blocked", "Imagens bloqueadas (375): nomes, preços e textos legíveis, sem rolagem horizontal, cartões mantêm proporção")
        def _():
            c = browser.new_context(viewport={"width": 375, "height": 667})
            pg = c.new_page()
            pg.route(re.compile(r".*\.(webp|jpg|jpeg|png)(\?.*)?$"), lambda r: r.abort())
            pg.goto(URL); pg.wait_for_load_state("load"); pg.wait_for_timeout(500)
            try:
                info = pg.evaluate("""() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
                    names: [...document.querySelectorAll('.card__name, .carousel__track h4')].filter(e => e.getBoundingClientRect().height > 0).length,
                    prices: [...document.querySelectorAll('.carousel__track > li')].filter(li => /R\\$ \\d/.test(li.innerText)).length,
                    mediaHeights: [...document.querySelectorAll('.card__media')].slice(0,3).map(m => Math.round(m.getBoundingClientRect().height))})""")
                pg.screenshot(path=str(SHOTS / "imagens-bloqueadas-375-full.png"), full_page=True)
                assert info["sw"] <= info["cw"] and info["names"] == 20 and info["prices"] == 20 and all(hh > 50 for hh in info["mediaHeights"]), info
                return info
            finally:
                c.close()

        # ---------- T24 espaçamento de texto (WCAG 1.4.12) ----------
        @run("T24-text-spacing", "Espaçamento de texto 1.4.12 (375): sem rolagem horizontal e sem texto cortado em botões/links")
        def _():
            c, pg = new_page(browser, 375, 667)
            try:
                pg.add_style_tag(content="* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; } p { margin-bottom: 2em !important; }")
                pg.wait_for_timeout(400)
                info = pg.evaluate("""() => { const clipped = [...document.querySelectorAll('a, button, h1, h2, h3, h4, p, summary, .tag')].filter(e => {
                      if (e.closest('[hidden], [data-drawer], .sr-only, [aria-hidden="true"]')) return false; const cs = getComputedStyle(e);
                      if (!e.getBoundingClientRect().width) return false;
                      return (cs.overflow !== 'visible' || cs.overflowX !== 'visible') && (e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1) && !e.classList.contains('carousel__track'); })
                    .map(e => ({tag: e.tagName, cls: e.className && e.className.baseVal === undefined ? e.className : '', text: e.textContent.trim().slice(0, 30)}));
                    return {sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, clipped: clipped.slice(0, 10)}; }""")
                pg.screenshot(path=str(SHOTS / "espacamento-texto-375.png"), full_page=False)
                assert info["sw"] <= info["cw"] and not info["clipped"], info
                return info
            finally:
                c.close()

        browser.close()

    summary = {s: sum(1 for r in RESULTS if r["status"] == s) for s in ("PASS", "FAIL", "ERROR", "NOT_RUN", "KNOWN_P3")}
    (OUT / f"results-{TAG}.json").write_text(json.dumps({"meta": meta, "summary": summary, "results": RESULTS}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("SUMMARY", summary)


if __name__ == "__main__":
    main()
