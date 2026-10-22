import json
from playwright.sync_api import sync_playwright
OUT='/home/claude/eixo-piloto-01/evidence/QUAL-001/'
URL='http://127.0.0.1:8765/index.html'
AXE=open('/tmp/claude-0/-home-claude/ccc621f2-8dc4-5dad-8106-d1347f352e12/scratchpad/axe/package/axe.min.js').read()
R={}
def focusinfo(pg):
    return pg.evaluate('''()=>{const e=document.activeElement;const b=e.getBoundingClientRect();const cs=getComputedStyle(e);
      const hdr=document.querySelector('[data-header]').getBoundingClientRect();
      return {tag:e.tagName,name:(e.getAttribute('aria-label')||e.innerText||'').trim().replace(/\\s+/g,' ').slice(0,50),top:Math.round(b.top),bottom:Math.round(b.bottom),outline:cs.outlineStyle+' '+cs.outlineWidth+' '+cs.outlineColor,hdrBottom:Math.round(hdr.bottom),obscured:b.bottom<=hdr.bottom}}''')
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    # ---- mobile flows
    ctx=b.new_context(viewport={'width':375,'height':812}); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(1200)
    m={}
    pg.keyboard.press('Tab'); m['tab1']=focusinfo(pg); pg.screenshot(path=OUT+'int-375-skiplink.png')
    pg.click('[data-open-menu]'); pg.wait_for_timeout(500)
    pg.screenshot(path=OUT+'int-375-menu.png')
    m['menu_focus']=focusinfo(pg)
    seq=[]
    for i in range(25):
        pg.keyboard.press('Tab'); f=focusinfo(pg); seq.append(f['name'])
    m['menu_tabseq']=seq
    m['menu_inside']=pg.evaluate("document.querySelector('#menu').contains(document.activeElement)")
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    m['after_esc']=focusinfo(pg); m['menu_hidden']=pg.evaluate("document.querySelector('#menu').hidden")
    # add to cart
    pg.locator('#novidades [data-add]').first.scroll_into_view_if_needed()
    pg.locator('#novidades [data-add]').first.click(); pg.wait_for_timeout(600)
    pg.screenshot(path=OUT+'int-375-added.png')
    m['toast']=pg.inner_text('[data-toast]'); m['count']=pg.inner_text('[data-cart-count]')
    m['focus_after_add']=focusinfo(pg)
    pg.locator('#novidades [data-add]').nth(3).click(); pg.wait_for_timeout(300)
    pg.click('[data-open-cart]'); pg.wait_for_timeout(600)
    pg.screenshot(path=OUT+'int-375-cart.png')
    m['cart_text']=pg.inner_text('#sacola')[:800]
    pg.click('[data-checkout]'); pg.wait_for_timeout(400)
    pg.screenshot(path=OUT+'int-375-checkout.png')
    m['notice']=pg.inner_text('[data-checkout-notice]')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    # filter
    pg.locator('#categorias [data-filter]').nth(1).scroll_into_view_if_needed()
    pg.locator('#categorias [data-filter]').nth(1).click(); pg.wait_for_timeout(700)
    pg.screenshot(path=OUT+'int-375-filter.png')
    m['filterbar']=pg.evaluate("(()=>{const f=document.querySelector('[data-filterbar]');return f?{hidden:f.hidden,text:f.innerText,top:f.getBoundingClientRect().top}:null})()")
    m['scrollY_after_filter']=pg.evaluate('scrollY')
    m['visible_cards']=pg.evaluate("[...document.querySelectorAll('.carousel__track > *')].filter(c=>c.offsetParent!==null).length")
    R['375']=m; ctx.close()
    # ---- desktop keyboard
    ctx=b.new_context(viewport={'width':1440,'height':900}); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(1200)
    seq=[]
    for i in range(45):
        pg.keyboard.press('Tab'); f=focusinfo(pg); seq.append(f)
        if i in (2,8,14,20,30): pg.screenshot(path=OUT+f'int-1440-focus-{i}.png')
    R['1440_tab']=seq
    # carousel arrows
    R['arrows_after_tab']=pg.evaluate("[...document.querySelectorAll('#novidades [data-dir]')].map(b=>b.getAttribute('aria-disabled'))+'|scrollLeft='+document.querySelector('#novidades .carousel__track').scrollLeft")
    pg.reload(); pg.wait_for_timeout(1200)
    R['arrows_fresh']=pg.evaluate("[...document.querySelectorAll('#novidades [data-dir]')].map(b=>b.getAttribute('aria-disabled'))")
    nx=pg.locator('#novidades [data-dir]').nth(1); nx.scroll_into_view_if_needed(); nx.click(); pg.wait_for_timeout(900)
    pg.locator('#novidades').screenshot(path=OUT+'int-1440-carousel-p2.png')
    R['arrows']=pg.evaluate("[...document.querySelectorAll('#novidades [data-dir]')].map(b=>({l:b.getAttribute('aria-label'),dis:b.disabled||b.getAttribute('aria-disabled')}))")
    R['bullets']=pg.evaluate("[...document.querySelectorAll('#novidades .carousel__dots button, #novidades [class*=dot]')].slice(0,6).map(b=>({t:b.tagName,l:b.getAttribute('aria-label'),cur:b.getAttribute('aria-current')||b.getAttribute('aria-selected'),w:b.getBoundingClientRect().width,h:b.getBoundingClientRect().height}))")
    pg.add_script_tag(content=AXE)
    R['axe_1440']=pg.evaluate("axe.run({runOnly:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}).then(r=>({v:r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,t:v.nodes.slice(0,3).map(n=>n.target.join(' '))})),inc:r.incomplete.map(v=>v.id+':'+v.nodes.length)}))")
    ctx.close()
    for w in (375,320):
        ctx=b.new_context(viewport={'width':w,'height':800}); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(1000)
        pg.add_script_tag(content=AXE)
        R[f'axe_{w}']=pg.evaluate("axe.run({runOnly:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}).then(r=>({v:r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,t:v.nodes.slice(0,3).map(n=>n.target.join(' '))})),inc:r.incomplete.map(v=>v.id+':'+v.nodes.length)}))")
        R[f'hscroll_{w}']=pg.evaluate('document.documentElement.scrollWidth')
        if w==320: pg.screenshot(path=OUT+'full-320.png',full_page=True)
        ctx.close()
    # zoom 200% ~ 640 css px at 1280; text spacing
    ctx=b.new_context(viewport={'width':640,'height':400}); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(1000)
    pg.add_style_tag(content='*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important} p{margin-bottom:2em!important}')
    pg.wait_for_timeout(300); R['textspacing_hscroll']=pg.evaluate('document.documentElement.scrollWidth')
    pg.screenshot(path=OUT+'int-640-textspacing.png',full_page=True); ctx.close()
    # reduced motion
    ctx=b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce'); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(800)
    R['rm_anims']=pg.evaluate("document.getAnimations().filter(a=>a.playState==='running').length"); ctx.close()
    ctx=b.new_context(viewport={'width':1440,'height':900}); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(2500)
    R['anims_default']=pg.evaluate("document.getAnimations().filter(a=>a.playState==='running').map(a=>a.animationName||'?')")
    pg.click('[data-pause-motion]'); pg.wait_for_timeout(300)
    R['anims_after_pause']=pg.evaluate("document.getAnimations().filter(a=>a.playState==='running').length")
    R['pause_label']=pg.evaluate("(()=>{const b=document.querySelector('[data-pause-motion]');return b.innerText+'|'+b.getAttribute('aria-pressed')})()")
    ctx.close()
    # no-js
    ctx=b.new_context(viewport={'width':375,'height':812},java_script_enabled=False); pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(800)
    pg.screenshot(path=OUT+'int-375-nojs.png'); R['nojs_menu_btn_visible']=pg.is_visible('[data-open-menu]'); ctx.close()
    b.close()
json.dump(R,open(OUT+'interactions.json','w'),ensure_ascii=False,indent=1)
