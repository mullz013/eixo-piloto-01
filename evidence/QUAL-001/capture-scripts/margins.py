import json
from playwright.sync_api import sync_playwright
out={}
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for w in (320,375,414,768,1024,1440):
        pg=br.new_page(viewport={'width':w,'height':900}); pg.goto('http://127.0.0.1:8765/index.html'); pg.wait_for_timeout(700)
        out[w]=pg.evaluate('''()=>{const vw=document.documentElement.clientWidth;const R=s=>{const e=document.querySelector(s);if(!e||e.offsetParent===null)return null;const b=e.getBoundingClientRect();return {l:+b.left.toFixed(1),r:+(vw-b.right).toFixed(1),t:+(b.top+scrollY).toFixed(1),b:+(b.bottom+scrollY).toFixed(1)}};
          const hero=R('.hero'), hdr=R('[data-header]'), perks=R('.perks > *')||R('.perks');
          const o={vw,hero,hdr,perks:R('.perks .wrap > *')||perks,menuBtn:R('[data-open-menu]'),bag:R('[data-open-cart]'),logo:R('.brand'),
           atelie:R('.atelie .wrap > *')||R('#atelie > *'),faq:R('#ajuda details'),footer:R('.footer > *'),heroCopy:R('.hero__copy'),
           heroTag:R('.hero .tag'),pause:R('[data-pause-motion]'),secTitle:R('#novidades .sec__title'),track:R('#novidades .carousel__track'),
           broken:[...document.images].filter(i=>!i.getAttribute('src')).map(i=>({cls:i.className,parent:i.parentElement.className,vis:i.offsetParent!==null}))};
          o.heroGapTop=hero&&hdr?+(hero.t-hdr.b).toFixed(1):null; o.heroGapBottom=hero&&o.perks?+(o.perks.t-hero.b).toFixed(1):null;
          return o}''')
        pg.close()
    br.close()
json.dump(out,open('/home/claude/eixo-piloto-01/evidence/QUAL-001/margins.json','w'),indent=1)
for w,o in out.items():
    print(w,'hero',o['hero'],'gapTop',o['heroGapTop'],'gapBot',o['heroGapBottom'])
    for k in ['hdr','menuBtn','bag','logo','perks','atelie','faq','footer','heroCopy','heroTag','pause','secTitle','track']: print('   ',k,o[k])
    print('   broken',o['broken'])
