from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=br.new_page(viewport={'width':1440,'height':900}); pg.goto('file:///home/claude/eixo-piloto-01/site/index.html'); pg.wait_for_timeout(2000)
    print(pg.evaluate("[...document.fonts].map(f=>f.family+' '+f.style+' '+f.status)"))
    pg.screenshot(path='/home/claude/eixo-piloto-01/evidence/QUAL-001/fold-1440-file-protocol.png')
    br.close()
