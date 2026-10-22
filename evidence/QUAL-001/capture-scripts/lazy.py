from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=br.new_page(viewport={'width':1440,'height':900}); pg.goto('http://127.0.0.1:8765/index.html'); pg.wait_for_timeout(800)
    q="[...document.querySelectorAll('#colecoes img')].slice(0,3).map(i=>({c:i.complete,nw:i.naturalWidth,lz:i.loading,op:getComputedStyle(i).opacity,src:(i.currentSrc||'').split('/').pop()}))"
    print('before',pg.evaluate(q))
    pg.evaluate("document.querySelector('#colecoes').scrollIntoView()"); pg.wait_for_timeout(1500)
    print('after scroll',pg.evaluate(q))
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
    pg.screenshot(path='/home/claude/eixo-piloto-01/evidence/QUAL-001/full-1440-after-lazyload.png',full_page=True)
    br.close()
