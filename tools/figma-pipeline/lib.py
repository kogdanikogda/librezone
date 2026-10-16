from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/'
EXP="""(()=>{const st=document.getElementById('__exp')||document.createElement('style');st.id='__exp';st.textContent='.phone{height:auto!important;min-height:844px}.phone .demo{display:none!important}.phone .content{overflow:visible!important;height:auto!important;max-height:none!important;flex:none!important}';document.head.appendChild(st)})()"""
UNEXP="(()=>{const s=document.getElementById('__exp');if(s)s.remove()})()"
def start(p,w=1300):
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':1000}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+S+'t_v3.html'); pg.wait_for_timeout(600)
    return b,pg,errs
def demo(pg,d,t=400):
    pg.evaluate("document.querySelector('[data-demo=\"%s\"]').click()"%d); pg.wait_for_timeout(t)
def shot(pg,name,full=True):
    if full: pg.evaluate(EXP); pg.wait_for_timeout(150)
    pg.locator('.phone').first.screenshot(path=S+'ref3/'+name+'.png')
    if full: pg.evaluate(UNEXP)
def act(pg,sel,t=500):
    pg.evaluate("(s=>{const e=document.querySelector(s);if(!e)throw new Error('no '+s);e.click()})('%s')"%sel.replace("'","\\'")); pg.wait_for_timeout(t)
def acts(pg):
    return pg.evaluate("[...document.querySelector('.phone').querySelectorAll('[data-act]')].map(e=>e.dataset.act+' | '+(e.innerText||'').trim().slice(0,30).replace(/\\n/g,' '))")
