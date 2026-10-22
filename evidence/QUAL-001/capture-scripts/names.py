from playwright.sync_api import sync_playwright
OUT='/home/claude/eixo-piloto-01/evidence/QUAL-001/'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':1440,'height':900}); pg.goto('http://127.0.0.1:8765/index.html'); pg.wait_for_timeout(800)
    cdp=pg.context.new_cdp_session(pg)
    t=cdp.send('Accessibility.getFullAXTree')['nodes']
    seen=set(); lines=[]
    for n in t:
        r=n.get('role',{}).get('value'); nm=n.get('name',{}).get('value','')
        if r in ('button','link','heading','region','navigation','complementary','status','img','list','banner','contentinfo','main') and not n.get('ignored'):
            k=(r,nm)
            if k in seen: continue
            seen.add(k); lines.append(f'{r}: {nm!r}')
    open(OUT+'ax-names-1440.txt','w').write('\n'.join(lines)); print('\n'.join(lines))
    # focus visibility with settle time
    res=[]
    for i in range(16):
        pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
        res.append(pg.evaluate('''()=>{const e=document.activeElement,b=e.getBoundingClientRect(),h=document.querySelector('[data-header]').getBoundingClientRect();return [(e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,25),Math.round(b.top),Math.round(b.bottom),Math.round(h.bottom),innerHeight]}'''))
        if i==12: pg.screenshot(path=OUT+'int-1440-focus-category.png')
    for r in res: print(r)
    b.close()
