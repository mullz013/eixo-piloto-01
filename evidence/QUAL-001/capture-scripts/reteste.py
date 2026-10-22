import json,io,re
from PIL import Image
from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8766/index.html'
OUT='/home/claude/eixo-piloto-01/evidence/QUAL-001/reteste/'
CH='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
def lum(c):
    f=lambda v:(v/255)/12.92 if v/255<=0.03928 else (((v/255)+0.055)/1.055)**2.4
    r,g,b=c[:3]; return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def ratio(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
res={'margins':{},'contrast':{},'names':{},'focus':None}
with sync_playwright() as p:
    br=p.chromium.launch(executable_path=CH)
    # P2-1 margins
    for w in (320,375,768,1024,1280,1440,1920):
        pg=br.new_page(viewport={'width':w,'height':900}); pg.goto(U); pg.wait_for_timeout(700)
        res['margins'][w]=pg.evaluate('''()=>{const vw=document.documentElement.clientWidth;const h=document.querySelector('.hero').getBoundingClientRect(),hd=document.querySelector('[data-header]').getBoundingClientRect(),pk=document.querySelector('.perks .wrap > *').getBoundingClientRect();
          return {vw,top:+(h.top-hd.bottom).toFixed(2),left:+h.left.toFixed(2),right:+(vw-h.right).toFixed(2),bottom:+(pk.top-h.bottom).toFixed(2),heroH:+h.height.toFixed(1)}}''')
        pg.close()
    # P2-2 contrast, mist at two positions
    for w,h in [(1280,800),(1440,900),(1920,1080)]:
        res['contrast'][w]={}
        for label,frac in [('mist_t0',0.0),('mist_t50',0.5),('mist_t100',1.0)]:
            pg=br.new_page(viewport={'width':w,'height':h}); pg.goto(U); pg.wait_for_timeout(1200)
            info=pg.evaluate('''(frac)=>{const out=[];document.getAnimations().forEach(a=>{a.pause();const n=a.animationName||'';const t=a.effect.getTiming();const d=typeof t.duration==='number'?t.duration:0;
              if(n==='drift'){a.currentTime=frac*d;}else{a.currentTime=(t.delay||0)+d*(t.iterations===Infinity?1:t.iterations)-1;} out.push([n,a.currentTime]);});return out}''',frac)
            pg.wait_for_timeout(150)
            bx=pg.evaluate('''()=>{const e=document.querySelector('.hero__lead');const r=document.createRange();r.selectNodeContents(e);const rects=[...r.getClientRects()].map(b=>({x:b.x,y:b.y,w:b.width,h:b.height}));return {color:getComputedStyle(e).color,fs:getComputedStyle(e).fontSize,rects}}''')
            pg.add_style_tag(content='.hero__copy *{color:transparent!important;-webkit-text-fill-color:transparent!important}')
            pg.wait_for_timeout(150)
            img=Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
            pg.close()
            col=tuple(int(float(v)) for v in re.findall(r'[\d.]+',bx['color'])[:3])
            px=[]
            for r in bx['rects']:
                for i in range(0,int(r['w']),2):
                    for j in range(0,int(r['h']),2):
                        X,Y=int(r['x']+i),int(r['y']+j)
                        if 0<=X<w and 0<=Y<h: px.append(img.getpixel((X,Y)))
            rs=sorted(ratio(col,c) for c in px)
            res['contrast'][w][label]={'color':col,'fontSize':bx['fs'],'lines':len(bx['rects']),'n':len(rs),'min':round(rs[0],2),'p5':round(rs[len(rs)//20],2),'median':round(rs[len(rs)//2],2),'animations':info}
    # P2-3 names via AX tree, P3-10, P3-4
    for w in (1440,375):
        pg=br.new_page(viewport={'width':w,'height':900}); pg.goto(U); pg.wait_for_timeout(800)
        cdp=pg.context.new_cdp_session(pg)
        def ax():
            t=cdp.send('Accessibility.getFullAXTree')['nodes']
            return [(n.get('role',{}).get('value'),n.get('name',{}).get('value','')) for n in t if not n.get('ignored')]
        nodes=ax()
        btn=[nm for r,nm in nodes if r=='button']
        d={'add':[n for n in btn if n.startswith('Adicionar')],'esgotado':[n for n in btn if n.startswith('Esgotado')],
           'brand':[nm for r,nm in nodes if r=='link' and 'Ateli' in nm and 'início' in nm],'bag':[n for n in btn if n.startswith('Sacola')]}
        visible=pg.evaluate('''()=>[...document.querySelectorAll('button.add:not([disabled])')].slice(0,2).map(b=>{const l=b.querySelector('.add__long'),s=b.querySelector('.add__short');return {long:l.offsetParent?l.textContent:null,short:s.offsetParent?s.textContent:null}})''')
        d['visibleLabel']=visible
        b=pg.locator('#novidades button.add').first; b.scroll_into_view_if_needed(); b.click(); pg.wait_for_timeout(200)
        nodes2=ax(); d['afterClick']=[nm for r,nm in nodes2 if r=='button' and nm.startswith('Adicionada')]
        d['bagAfter']=[nm for r,nm in nodes2 if r=='button' and nm.startswith('Sacola')]
        pg.keyboard.press('Escape'); pg.wait_for_timeout(1800)
        d['afterRevert']=pg.locator('#novidades button.add').first.get_attribute('aria-label')
        res['names'][w]=d
        pg.close()
    pg=br.new_page(viewport={'width':1440,'height':900}); pg.goto(U); pg.wait_for_timeout(800)
    seq=[]
    for i in range(14):
        pg.keyboard.press('Tab'); pg.wait_for_timeout(120)
        seq.append(pg.evaluate("()=>{const e=document.activeElement;return (e.getAttribute('aria-label')||e.innerText||'').trim().replace(/\\s+/g,' ').slice(0,40)}"))
    res['focus']=seq; pg.close()
    for w,h in [(375,667),(1440,900),(320,568),(768,1024)]:
        pg=br.new_page(viewport={'width':w,'height':h}); pg.goto(U); pg.wait_for_timeout(1800)
        pg.screenshot(path=OUT+f'fold-{w}x{h}.png')
        res.setdefault('fold',{})[f'{w}x{h}']=pg.evaluate('''()=>{const c=document.querySelector('.hero__cta .btn').getBoundingClientRect();const s=document.querySelector('.hero__stage').getBoundingClientRect();return {ctaBottom:Math.round(c.bottom),innerH:innerHeight,ctaInFold:c.bottom<=innerHeight,stageH:Math.round(s.height)}}''')
        pg.close()
    br.close()
json.dump(res,open(OUT+'raw.json','w'),indent=1,ensure_ascii=False)
print(json.dumps(res,indent=1,ensure_ascii=False))
