import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ref3/'
ids=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844})
    for i in ids:
        pg.goto('file://'+S+'prev/%s.html'%i);pg.wait_for_timeout(200)
        r=pg.evaluate("""(()=>{const root=document.querySelector('body>div>div');const R=root.getBoundingClientRect();const out=[];
        for(const e of document.querySelectorAll('[data-a]')){const a=e.dataset.a.split(',').map(Number);const r=e.getBoundingClientRect();const d=[r.x-R.x-a[0],r.y-R.y-a[1],r.width-a[2],r.height-a[3]].map(v=>Math.round(v));
          if(Math.abs(d[0])>3||Math.abs(d[1])>3||Math.abs(d[3])>3||(Math.abs(d[2])>3)){let path=[];let x=e;while(x&&x!==root){if(x.title)path.unshift(x.title);x=x.parentElement}out.push(path.join('>')+' d='+d.join(','))}}return out})()""")
        print('==',i,len(r))
        for x in r[:12]:print('  ',x)
