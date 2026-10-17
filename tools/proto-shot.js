const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox']});
const pg=await b.newPage({viewport:{width:430,height:900}});await pg.route(/^https?:/,r=>r.abort());
await pg.goto('file:///home/claude/librezone/prototype/libre-zone-v3.html');await pg.waitForTimeout(700);
await pg.screenshot({path:'/tmp/s1.png'});
await pg.evaluate(()=>document.querySelector('#phone [data-act="home-continue"]').click());await pg.waitForTimeout(500);
await pg.screenshot({path:'/tmp/s2.png'});await b.close()})()
