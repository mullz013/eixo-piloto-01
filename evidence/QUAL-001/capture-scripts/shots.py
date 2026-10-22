import json,sys
from playwright.sync_api import sync_playwright
OUT='/home/claude/eixo-piloto-01/evidence/QUAL-001/'
URL='http://127.0.0.1:8765/index.html'
res={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for w,h in [(375,812),(768,1024),(1440,900)]:
        ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1)
        pg=ctx.new_page()
        errs=[]
        pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        pg.on('requestfailed',lambda r: errs.append('FAIL '+r.url))
        pg.goto(URL); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(1500)
        # trigger lazy images
        H=pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,500):
            pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(80)
        pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(800)
        pg.screenshot(path=f'{OUT}full-{w}.png',full_page=True)
        pg.screenshot(path=f'{OUT}fold-{w}.png')
        for sel,name in [('.hero','hero'),('.perks','perks'),('#categorias','categorias'),('#novidades','novidades'),('#atelie','atelie'),('#colecoes','colecoes'),('#ajuda','ajuda'),('.footer','footer')]:
            el=pg.query_selector(sel)
            if el:
                el.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
                el.screenshot(path=f'{OUT}sec-{w}-{name}.png')
        m=pg.evaluate('''()=>{
          const r=s=>{const e=document.querySelector(s); if(!e) return null; const b=e.getBoundingClientRect(); return {x:b.x,w:b.width,right:innerWidth-b.right,h:b.height}};
          const vw=document.documentElement.clientWidth;
          const out={vw, scrollW:document.documentElement.scrollWidth, innerW:innerWidth};
          for(const s of ['.hero','.perks','#categorias','#novidades','#atelie','#colecoes','#ajuda','.footer','.header__in','.announce']) out[s]=r(s);
          // titles
          out.titles=[...document.querySelectorAll('h1,h2,h3')].map(e=>{const cs=getComputedStyle(e);return {t:e.textContent.trim().slice(0,60),fs:cs.fontSize,fw:cs.fontWeight,ff:cs.fontFamily.slice(0,20),vis:e.offsetParent!==null}});
          // carousels
          out.tracks=[...document.querySelectorAll('[data-track], .track, .carousel__track')].map(t=>{const tb=t.getBoundingClientRect(); const cards=[...t.children].map(c=>c.getBoundingClientRect()); const fully=cards.filter(c=>c.left>=tb.left-1&&c.right<=Math.min(tb.right,innerWidth)+1).length; const partial=cards.filter(c=>c.left<innerWidth&&c.right>innerWidth).map(c=>(innerWidth-c.left)/c.width); return {cls:t.className,n:cards.length,fully,partial,left:tb.left,cardW:cards[0]&&cards[0].width}});
          // badges
          out.badges=[...document.querySelectorAll('[class*=badge],[class*=kicker],[class*=tag],[class*=eyebrow],[class*=pill]')].slice(0,30).map(e=>{const cs=getComputedStyle(e);return {c:e.className,t:e.textContent.trim().slice(0,40),br:cs.borderRadius,fs:cs.fontSize,bg:cs.backgroundColor,bd:cs.borderTopWidth+' '+cs.borderTopColor,vis:e.offsetParent!==null}});
          // small tap targets
          out.small=[...document.querySelectorAll('a,button,summary,[tabindex]')].filter(e=>e.offsetParent!==null).map(e=>{const b=e.getBoundingClientRect();return {t:(e.getAttribute('aria-label')||e.textContent).trim().slice(0,40),w:Math.round(b.width),h:Math.round(b.height)}}).filter(o=>o.w<24||o.h<24);
          // small text
          const sm=new Set(); document.querySelectorAll('body *').forEach(e=>{if(e.offsetParent===null) return; const fs=parseFloat(getComputedStyle(e).fontSize); if(fs<13 && [...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())) sm.add(e.className+':'+fs+':'+e.textContent.trim().slice(0,30))}); out.smallText=[...sm];
          out.imgs=[...document.images].map(i=>({s:i.currentSrc.split('/').slice(-2).join('/'),ok:i.complete&&i.naturalWidth>0,alt:i.alt})).filter(i=>!i.ok);
          return out}''')
        m['errors']=errs
        res[w]=m
        ctx.close()
    b.close()
json.dump(res,open(OUT+'measures.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False)[:200])
