from playwright.sync_api import sync_playwright
O='/home/claude/eixo-piloto-01/evidence/QUAL-001/'
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=br.new_page(viewport={'width':1440,'height':900}); pg.goto('http://127.0.0.1:8765/index.html'); pg.wait_for_timeout(800)
    pg.keyboard.press('Tab')
    for i in range(7): pg.keyboard.press('Tab')
    pg.keyboard.press('Enter'); pg.wait_for_timeout(600)
    pg.screenshot(path=O+'int-1440-cart-empty.png')
    print(pg.evaluate("document.activeElement.innerText||document.activeElement.getAttribute('aria-label')"))
    seq=[]
    for i in range(6):
        pg.keyboard.press('Tab'); seq.append(pg.evaluate("(document.activeElement.innerText||document.activeElement.getAttribute('aria-label')||document.activeElement.tagName).trim()"))
    print(seq)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    print('after esc',pg.evaluate("document.activeElement.getAttribute('aria-label')||document.activeElement.innerText"))
    br.close()
