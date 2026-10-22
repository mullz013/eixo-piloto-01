import json,io
from PIL import Image
from playwright.sync_api import sync_playwright
def lum(c):
    def f(v):
        v/=255; return v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    r,g,b=c[:3]; return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def ratio(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
out={}
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for w,h in [(1440,900),(375,812),(768,1024)]:
        pg=br.new_page(viewport={'width':w,'height':h},reduced_motion='reduce'); pg.goto('http://127.0.0.1:8765/index.html'); pg.wait_for_timeout(1500)
        sels=['.hero__lead','.hero__title','.hero .tag','.hero [data-pause-motion]','.hero .btn--ghost, .hero a:not(.btn)']
        boxes=pg.evaluate('''(sels)=>sels.map(s=>{const e=document.querySelector(s); if(!e) return null; const b=e.getBoundingClientRect(); const cs=getComputedStyle(e); return {s, x:b.x,y:b.y,w:b.width,h:b.height,color:cs.color}})''',sels)
        pg.add_style_tag(content='.hero__copy *, .hero [data-pause-motion]{color:transparent!important;-webkit-text-fill-color:transparent!important}')
        pg.wait_for_timeout(200)
        img=Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
        res=[]
        for bx in boxes:
            if not bx: continue
            import re
            col=tuple(int(float(v)) for v in re.findall(r'[\d.]+',bx['color'])[:3])
            px=[]
            for i in range(0,int(bx['w']),4):
                for j in range(0,int(bx['h']),4):
                    X,Y=int(bx['x']+i),int(bx['y']+j)
                    if 0<=X<w and 0<=Y<h: px.append(img.getpixel((X,Y)))
            if not px: continue
            rs=sorted(ratio(col,c) for c in px)
            res.append({'sel':bx['s'],'color':col,'min':round(rs[0],2),'p5':round(rs[len(rs)//20],2),'median':round(rs[len(rs)//2],2)})
        out[w]=res
        pg.close()
    br.close()
json.dump(out,open('/home/claude/eixo-piloto-01/evidence/QUAL-001/hero-contrast-sampled.json','w'),indent=1)
print(json.dumps(out,indent=1))
