const {chromium}=require('playwright');
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox']});
const pg=await b.newPage({viewport:{width:430,height:900}});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///home/claude/librezone/prototype/libre-zone-v3.html');await pg.waitForTimeout(600);
const scan=()=>pg.evaluate(()=>{
 const P='в|во|к|ко|с|со|у|о|об|от|до|на|по|за|из|не|ни|но|да|для|при|без|над|под|про|или|что|как|а|и|я';
 const rx=[new RegExp('(^|[ («])('+P+') \\S','i'),/\d \d{3}(?!\d)/,/ [—–] /,/\d [A-Za-zА-Яа-я₽%$€]/,/ (же|ли|бы)[ .,]/,/\.\.\./];
 const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const p=n.parentNode;if(/SCRIPT|STYLE/.test(p.nodeName)||p.closest('.mono,[data-notypo]'))continue;
  const el=p.closest('*');if(!(p.offsetParent||p.getClientRects().length))continue;
  const t=n.nodeValue;rx.forEach((r,i)=>{if(r.test(t))out.push(i+': '+t.trim().slice(0,70))})}
 return out});
let reloads=0;await pg.route(/^https?:/,r=>r.abort());const seen=new Set();let all=new Set(),clicks=0;
for(let round=0;round<400;round++){
 (await scan()).forEach(x=>all.add(x));
 const btns=await pg.$$('#phone [data-act], #phone [data-demo]');let did=false;
 for(const bt of btns){const k=await bt.evaluate(e=>e.dataset.act+'|'+(e.textContent||'').trim().slice(0,20)+'|'+(e.dataset.v||''));
  if(seen.has(k)||/logout|copy|share/.test(k))continue;
  seen.add(k);
  try{await bt.evaluate(e=>e.click());did=true;clicks++;await pg.waitForTimeout(120);break}catch(e){}}
 if(!did){if(reloads++>=2)break;await pg.goto('file:///home/claude/librezone/prototype/libre-zone-v3.html',{waitUntil:'domcontentloaded'});await pg.waitForTimeout(400)}
 }
(await scan()).forEach(x=>all.add(x));
console.log('clicks',clicks,'errs',errs.slice(0,3));console.log([...all].join('\n')||'NO VIOLATIONS');
await pg.screenshot({path:'/tmp/shot.png'});await b.close()})();
