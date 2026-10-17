/* иконка рядом с текстом: по верхнему краю текста, при одной строке — по центру */
var IA_SEL='.dbody h3,.dcard,.card.rows .row,.wrow,.why,.notebox,.warnbox,.okbox,.hours .hh,.notify,.check,.eta,.opt,.dsum li,.u,.docnote,.plate,.tg,.timer .row';
var IA_SKIP=['n','ic','wi','wi2','hi','tok','sw','av','mini-copy','seg2','hstat','hst','tag','ptm','bul','dt','bdot','rubmark','ck'];
function textBlockOf(el){var c=el.children;for(var i=0;i<c.length;i++){var x=c[i];if(x.tagName==='svg'||x.tagName==='INPUT')continue;var skip=false;for(var j=0;j<IA_SKIP.length;j++)if(x.classList.contains(IA_SKIP[j])){skip=true;break}if(skip)continue;if(x.textContent.trim())return x}return null}
var ZM=1;
function alignIcons(root){if(!root)return;[].forEach.call(root.querySelectorAll(IA_SEL),function(el){var t=textBlockOf(el);if(!t)return;var cs=getComputedStyle(t),lh=parseFloat(cs.lineHeight);if(!lh){var f=t.querySelector('b,span,small');lh=f?parseFloat(getComputedStyle(f).lineHeight):20}if(!lh||isNaN(lh))lh=20;var h=t.getBoundingClientRect().height/ZM;el.classList.add('ia');el.classList.toggle('one',h<=lh*1.45)})}
/* сумма в калькуляторе не заходит под кнопку смены направления: длинное число уменьшается */
function fitAmts(){[].forEach.call(document.querySelectorAll('#app .crow .amt'),function(a){a.style.fontSize='';var fs=parseFloat(getComputedStyle(a).fontSize),min=17;while(a.scrollWidth>a.clientWidth+0.5&&fs>min){fs-=1;a.style.fontSize=fs+'px'}})}
function polish(){var a=$('#app'),l=$('#layer');typoTree(a);typoTree(l);alignIcons(a);alignIcons(l);fitAmts()}
function render(){DEMO=[];
 var h=S.screen==='docs'?docsHTML():S.screen==='doc'?docHTML():S.screen==='new'?newHTML():S.screen==='order'?orderHTML():S.screen==='orders'?ordersHTML():S.screen==='profile'?profileHTML():homeHTML();
 var of=document.querySelector('#app .filters'),fl=of?of.scrollLeft:0;
 var app=$('#app'),old=app.querySelector('#scroller'),top=old?old.scrollTop:0,same=app.dataset.screen===S.screen+S.step;
 var tabbed=['home','orders','profile'].indexOf(S.screen)>=0;if(tabbed)h+=tabsHTML();app.classList.toggle('tabbed',tabbed);app.classList.toggle('plated',tabbed&&!!plateHTML());
 app.innerHTML=h;app.dataset.screen=S.screen+S.step;
 var c=app.querySelector('#scroller');if(c&&same)c.scrollTop=top;
 if(c&&!same&&app.dataset.inited){var TI=['home','orders','profile'],rk=function(s){return TI.indexOf(s)>=0?0:1},ps=app.dataset.psc,pst=+app.dataset.pst,dr;
  if(S.screen!==ps){if(rk(S.screen)>rk(ps))dr='fwd';else if(rk(S.screen)<rk(ps))dr='back';else if(rk(S.screen)===0)dr=TI.indexOf(S.screen)>TI.indexOf(ps)?'tabr':'tabl';else dr='fwd'}else dr=S.step>pst?'fwd':'back';
  c.classList.add('en','en-'+dr);[].slice.call(c.children,0,9).forEach(function(e,i){e.style.setProperty('--i',i)});
  app.classList.add('switching');clearTimeout(app._sw);app._sw=setTimeout(function(){app.classList.remove('switching')},700)}
 app.dataset.inited=1;app.dataset.psc=S.screen;app.dataset.pst=S.step;
 renderLayer();sync();polish();demoPanel();
 var nf2=app.querySelector('.filters');if(nf2){nf2.scrollLeft=fl;var a=nf2.querySelector('[aria-pressed="true"]');if(a){var pl=16,l=a.offsetLeft-nf2.offsetLeft,r=l+a.offsetWidth,vl=nf2.scrollLeft,vr=vl+nf2.clientWidth,t=null;if(l-pl<vl)t=l-pl;else if(r+pl>vr)t=r+pl-nf2.clientWidth;if(t!==null)nf2.scrollTo({left:Math.max(0,t),behavior:'smooth'})}}
}
function demoPanel(){var c=$('#dctx');if(!c)return;
 c.hidden=!DEMO.length;c.innerHTML=DEMO.map(function(g){return '<div class="group"><span>'+esc(g[0])+'</span><div class="dc">'+g[1].map(function(x){return '<button class="dbtn" type="button" data-act="d:'+x[1]+'">'+esc(x[0])+'</button>'}).join('')+'</div></div>'}).join('');typoTree(c)}
function renderLayer(){var l=$('#layer'),lh=layerHTML();
 if(!lh&&l.firstElementChild&&!l._closing){l._closing=1;var o=l.firstElementChild;o.classList.add('out');setTimeout(function(){l._closing=0;if(!layerHTML()){l.innerHTML='';l.dataset.sig=''}},230);return}
 var sg=lh.slice(0,150);l.classList.toggle('still',!!lh&&l.dataset.sig===sg&&!l._closing);l.dataset.sig=lh?sg:'';l._closing=0;
 l.innerHTML=lh;typoTree(l);alignIcons(l);if(S.login){var f=l.querySelector('[data-code="0"]')||l.querySelector('#lph')||l.querySelector('#lfio');if(f)f.focus()}else if(S.sheet==='bank'){var q=l.querySelector('#bq');if(q)q.focus()}}
function go(screen){S.screen=screen;S.menu=false;S.sheet=null;S.modal=null;render();var c=$('#scroller');if(c)c.scrollTop=0}
function sync(){
 var b=$('#next');if(b)b.disabled=!readyStep1();
 var c=$('#create');if(c)c.disabled=!readyNew();
 var r=$('#sendr');if(r){var o=getOrder(S.openId);r.disabled=!(o&&/^https?:\/\/\S{6,}/.test((o.link||'').trim()))}
}
function startLogin(){S.login={step:'start',phone:'',err:false,resend:26,fio:'',email:''};renderLayer()}
function newOrder(){
 var buy=S.dir==='buy',a=cryptoAmt();
 var o={id:Math.random().toString(36).slice(2,11).toUpperCase(),dir:S.dir,giveCode:giveC(),getCode:getC(),give:buy?S.amount:a,get:buy?a:S.amount,bank:S.bank,addr:S.addr.trim(),status:'created',rem:600000,frem:1800000,stage:3500,nameOk:false,link:'',date:(function(){var x=new Date();return pad(x.getDate())+'.'+pad(x.getMonth()+1)+'.'+x.getFullYear()+', '+pad(x.getHours())+':'+pad(x.getMinutes())})()};
 S.orders.unshift(o);S.openId=o.id;S.bank=null;S.addr='';S.agree=false;S.step=1;go('order');
}
function tick(){
 var rerender=false;
 S.orders.forEach(function(o){
  if(o.status==='pay'){o.rem-=250*speedKeep;if(o.rem<=0){o.rem=0;o.status='error';o.err='nosend';rerender=true;if(S.screen==='order'&&S.openId===o.id)S.modal='timeout'}}
  else if(o.status==='fiat'){o.frem=Math.max(0,o.frem-250*speedKeep)}
  else if(o.status==='created'||o.status==='check'||o.status==='crypto'||o.status==='aml'){o.stage-=250;if(o.stage<=0){
   if(o.status==='created'){o.status='pay'}else if(o.status==='check'){o.status='crypto';o.stage=3500}else if(o.status==='aml'){o.status='fiat';o.frem=1800000}else{o.status='done';if(S.screen==='order'&&S.openId===o.id)referLater(o)}
   rerender=true}}
 });
 if(rerender&&(S.screen==='order'||S.screen==='orders'))render();
 var o2=S.screen==='order'?getOrder(S.openId):null,tv=$('#tval'),fv=$('#fval');
 if(o2&&o2.status==='pay'&&tv){tv.textContent=mmss(o2.rem);$('#tbar').style.width=Math.max(0,o2.rem/6000)+'%';$('#timer').classList.toggle('warn',o2.rem<=120000)}
 if(o2&&o2.status==='fiat'&&fv){fv.textContent=mmss(o2.frem);$('#ftimer').classList.toggle('warn',o2.frem<=300000)}
}
setInterval(tick,250);
setInterval(function(){var p=$('#ptm');if(!p)return;var o=getOrder(p.getAttribute('data-id'));if(!o||o.status!=='pay'){if(['home','orders','profile'].indexOf(S.screen)>=0)render();return}p.textContent=mmss(o.rem)},500);
setInterval(function(){var L=S.login;if(L&&L.step==='code'&&L.resend>0){L.resend--;var r=$('#resend');if(r)r.innerHTML=resendText(L);if(L.resend===0){var b=$('#rbtn');if(b)b.disabled=false}}},1000);

function repeatOrder(id){
 var o=getOrder(id);if(!o)return;
 S.dir=o.dir;S.coin=o.dir==='buy'?o.getCode:o.giveCode;
 var rub=o.dir==='buy'?o.give:o.get,best=CHIPS[0];CHIPS.forEach(function(v){if(v<=rub)best=v});S.amount=best;
 S.bank=o.bank;S.addr=o.addr;S.agree=false;S.step=1;
 if(!S.user){go('home');startLogin();return}
 go('new');toast('Реквизиты подставлены из прошлого обмена');
}
function fmtPhone(raw){var d=raw.replace(/\D/g,'');if(d[0]==='8')d='7'+d.slice(1);if(d&&d[0]!=='7')d='7'+d;d=d.slice(0,11);return d?'+'+d[0]+(d.length>1?' '+d.slice(1,4):'')+(d.length>4?' '+d.slice(4,7):'')+(d.length>7?'-'+d.slice(7,9):'')+(d.length>9?'-'+d.slice(9,11):''):''}
function setStatus(o,a){
 var buy=o.dir==='buy';
 if(a==='created'){o.status='created';o.stage=3600000}
 else if(a==='pay'){o.status='pay';o.rem=600000}
 else if(a==='soon'){o.status='pay';o.rem=90000}
 else if(a==='verify'){o.status=buy?'check':'aml';o.stage=3600000}
 else if(a==='wait'){if(buy){o.status='crypto';o.stage=3600000}else{o.status='fiat';o.frem=1800000}}
 else if(a==='done'){o.status='done';referLater(o)}
 else if(a==='timeout'){o.status='error';o.err='nosend';S.modal='timeout'}
 else if(a==='cancelled'){o.status='cancelled';o.err='user'}
 render();
}
function makeOrder(op){var buy=op.dir==='buy',c=op.coin||'TRX',rub=op.rub||5000,a=rub/CUR[c].rate;
 return {id:rid(),dir:op.dir,giveCode:buy?'RUB':c,getCode:buy?c:'RUB',give:buy?rub:a,get:buy?a:rub,bank:op.bank||'sber',addr:buy?CUR[c].ex:'+7 903 556-44-83',status:op.status||'pay',rem:op.rem||600000,frem:1800000,stage:3600000,nameOk:!!op.nameOk,link:'',date:nowStr()}}
function openNew(op){if(!S.user)S.user={};S.askLogin=false;pressed('auth','in');var o=makeOrder(op);S.orders.unshift(o);S.openId=o.id;go('order')}
function scenario(v){
 if(v==='buy-sber')openNew({dir:'buy',bank:'sber'});
 else if(v==='buy-tbank')openNew({dir:'buy',bank:'tbank',nameOk:true});
 else if(v==='sell-pay')openNew({dir:'sell',bank:'sber'});
 else if(v==='sell-fiat')openNew({dir:'sell',bank:'tbank',status:'fiat',rub:50000});
 else if(v==='late')openNew({dir:'buy',bank:'sber',nameOk:true,rem:90000});
 else if(v==='fail'){if(!S.user)S.user={};S.filter='failed';go('orders')}
}
function demoAct(v){
 var o=S.screen==='order'?getOrder(S.openId):null,p=v.split(':'),k=p[0],a=p[1],buy=S.dir==='buy';
 if(k==='bank'){S.bank=a;if(!buy)S.addr='';render();return}
 if(k==='addr'){
  if(a==='ok')S.addr=buy?CUR[S.coin].ex:'+7 903 556-44-83';
  else if(a==='card')S.addr='5536 9141 2345 6789';
  else if(a==='net')S.addr=CUR[S.coin==='ETH'?'TRX':'ETH'].ex;
  else if(a==='short')S.addr=buy?'T9yD14Nj9j7x':'+7 903 55';
  else if(a==='bad')S.addr='+7 903 556-44-833';
  if(!buy&&!S.bank)S.bank='sber';
  render();return}
 if(k==='agree'){S.agree=true;render();return}
 if(k==='calc'){
  if(a==='buy'){S.dir='buy';S.coin='TRX';S.amount=5000;resetReq()}
  else if(a==='sell'){S.dir='sell';S.coin='TRX';S.amount=50000;resetReq()}
  else if(a==='btc'){S.dir='buy';S.coin='BTC';S.amount=50000;resetReq()}
  else if(a==='eth'){S.dir='buy';S.coin='ETH';S.amount=10000;resetReq()}
  else if(a==='off'){S.working=false;pressed('mode','off')}
  else if(a==='on'){S.working=true;pressed('mode','on')}
  render();return}
 if(k==='st'&&o){setStatus(o,a);return}
 if(k==='err'&&o){o.status='error';o.err=a;render();return}
 if(k==='link'&&o){o.link=a==='ok'?'https://www.tbank.ru/cheque/7f3a9c21':'tbank.ru/cheque';render();return}
 if(k==='o'){S.orders.unshift(makeOrder({dir:a,bank:a==='buy'?'sber':'tbank'}));render();return}
 if(k==='prof'){S.profile.fio='Петрова Мария Сергеевна';S.profile.email='maria@libre.zone';render();return}
 if(k==='l'&&S.login){
  var L=S.login;
  if(a==='phone'){L.phone='+7 937 421-45-13';renderLayer()}
  else if(a==='short'){L.phone='+7 937';renderLayer()}
  else if(a==='codeok'||a==='codebad'){var cd=a==='codeok'?'123456':'000000';[].forEach.call(document.querySelectorAll('[data-code]'),function(x,i){x.value=cd.charAt(i)})}
  else if(a==='regok'){L.fio='Иванов Иван Иванович';L.email='ivan@libre.zone';renderLayer()}
  else if(a==='regbad'){L.fio='Иван';L.email='ivan@';renderLayer()}
 }
}
function resetReq(){S.bank=null;S.addr='';S.agree=false;S.step=1}

document.addEventListener('click',function(e){
 var dm=e.target.closest('[data-demo]');if(dm){demo(dm.getAttribute('data-demo'));return}
 var el=e.target.closest('[data-act]');
 if(!el)return;
 if(el.classList.contains('scrim')&&e.target!==el)return;
 var a=el.getAttribute('data-act'),p=a.split(':'),k=p[0],v=p.slice(1).join(':');
 if(el.tagName==='A')e.preventDefault();
 if(k==='tab'){go(v);return}
 if(k==='ptheme'){demo('theme:'+v);render();return}
 if(k==='lang'){if(v==='en')toast('Английская версия появится позже');return}
 if(k==='docs'){if(['docs','doc'].indexOf(S.screen)<0)S.docBack=S.screen;go('docs');return}
 if(k==='doc'){if(S.screen==='docs')S.docVia='list';else if(S.screen!=='doc'){S.docVia='direct';S.docBack=S.screen}S.doc=v;go('doc');return}
 if(k==='docback'){if(S.screen==='doc'&&S.docVia==='list'){go('docs');return}go(S.docBack||'profile');return}
 if(k==='dsec'){var t=document.getElementById('dsec'+v),sc=$('#scroller');if(t&&sc)sc.scrollTo({top:t.offsetTop-70,behavior:'smooth'});return}
 if(k==='logoutq'){S.modal='logoutq';renderLayer();return}
 if(k==='menu'){S.menu=!S.menu;renderLayer();return}
 if(k==='go'){
  if(v==='new'){if(!S.user){go('home');startLogin();return}S.step=1;go('new');return}
  go(v);return}
 if(k==='support'){S.modal=null;renderLayer();toast(v?'Откроется чат поддержки. Номер заявки '+v+' передан автоматически':'Откроется чат поддержки в Telegram');return}
 if(k==='partner'){toast('Откроется сайт партнёра: '+v);return}
 if(k==='sheet'){S.sheet=v;S.q='';renderLayer();return}
 if(k==='close'){S.sheet=null;S.modal=null;renderLayer();return}
 if(k==='coin'){S.coin=v;S.sheet=null;if(S.dir==='buy')S.addr='';render();return}
 if(k==='bank'){S.bank=v;S.sheet=null;S.q='';if(S.dir==='sell')S.addr='';render();return}
 if(k==='chip'){S.amount=CHIPS[+v];render();return}
 if(k==='sdot'){var w=$('#ssl');if(w){var it=w.children[+v];w.scrollTo({left:it.offsetLeft-w.offsetLeft-parseFloat(getComputedStyle(w).paddingLeft||0),behavior:'smooth'})}return}
 if(k==='wdot'){var w=$('#wsl');if(w){var it=w.children[+v];w.scrollTo({left:it.offsetLeft-w.offsetLeft-parseFloat(getComputedStyle(w).paddingLeft||0),behavior:'smooth'})}return}
 if(k==='swap'){S.dir=S.dir==='buy'?'sell':'buy';resetReq();render();var sb=$('.swapbtn');if(sb){sb.classList.add('rot')}return}
 if(k==='home-continue'){if(!S.user){startLogin();return}S.step=1;go('new');return}
if(k==='d'){demoAct(v);return}
 if(k==='fill'){if(!S.bank)S.bank='sber';S.addr=S.dir==='buy'?CUR[S.coin].ex:(bank(S.bank).link?'5536 9141 2345 6789':'+7 903 556-44-83');render();return}
 if(k==='edit-amount'){go('home');return}
 if(k==='newback'){if(S.step===2){S.step=1;render()}else go('home');return}
 if(k==='step2'){if(readyStep1()){S.step=2;render();var c=$('#scroller');if(c)c.scrollTop=0}return}
 if(k==='agree'){S.agree=el.checked;sync();return}
 if(k==='rules'){S.docVia='direct';S.docBack=S.screen;S.doc='rules';go('doc');return}
 if(k==='instr'||k==='why'){toast('Инструкции и FAQ в прототип не входят');return}
 if(k==='create'){newOrder();return}
 if(k==='notes'){if(!S.user){startLogin();return}S.sheet='notes';render();return}
 if(k==='notesread'){S.notes.forEach(function(n){n.read=true});render();return}
 if(k==='note'){var nn=S.notes[+v];nn.read=true;S.sheet=null;if(nn.o&&getOrder(nn.o)){S.openId=nn.o;go('order')}else if(nn.a==='new'){go('new')}else if(nn.a==='profile'){go('profile')}else if(nn.a&&nn.a.indexOf('doc:')===0){S.docBack=S.screen;S.docVia='direct';S.doc=nn.a.slice(4);go('doc')}else render();return}
 if(k==='open'){S.openId=v;go('order');return}
 if(k==='back'){go('orders');return}
 if(k==='filter'){S.filter=v;render();return}
 if(k==='repeat'){e.stopPropagation();repeatOrder(v);return}
 if(k==='notify'){S.notify=el.checked;toast(S.notify?'Уведомления в Telegram включены':'Уведомления выключены');return}
 if(k==='share'){toast('Откроется выбор чата в Telegram');return}
 if(k==='copy'){doCopy(v,el);return}
 if(k==='name'){var o=getOrder(S.openId);if(v==='yes'){o.nameOk=true;render()}else{S.modal='noname';renderLayer()}return}
 if(k==='sent'){var o2=getOrder(S.openId);o2.status=o2.dir==='buy'?'check':'aml';o2.stage=3500;render();return}
 if(k==='got'){var o4=getOrder(S.openId);if(v==='yes'){o4.status='done';referLater(o4)}else{o4.status='error';o4.err='norecv'}render();return}
 if(k==='cancel'){S.modal='confirm';renderLayer();return}
 if(k==='cancel-yes'){var o3=getOrder(S.openId);o3.status='cancelled';o3.err='user';S.modal=null;render();return}
 if(k==='to-profile'){S.modal=null;go('profile');return}
 if(k==='edit'){S.edit=true;S.saved=false;render();return}
 if(k==='save'){S.edit=false;S.saved=true;render();setTimeout(function(){S.saved=false;if(S.screen==='profile')render()},2000);return}
 if(k==='logout'){S.user=null;S.menu=false;S.modal=null;go('home');toast('Вы вышли из аккаунта');return}
 if(k==='lclose'){S.login=null;renderLayer();return}
 if(k==='lcancel'){S.login=null;renderLayer();return}
 if(!S.login&&/^l(start|phone|tg|code|check|finish|resend|cancel)$/.test(k))return;/* кнопка закрывающейся шторки входа */
 if(k==='lstart'){S.login.step='start';renderLayer();return}
 if(k==='lphone'){S.login.step='phone';renderLayer();return}
 if(k==='ltg'){S.login.step='tg';renderLayer();setTimeout(function(){if(S.login&&S.login.step==='tg'){S.login.phone='+7 937 421-45-13';S.login.step='reg';renderLayer()}},1300);return}
 if(k==='lcode'){S.login.step='code';S.login.err=false;S.login.resend=26;renderLayer();return}
 if(k==='lresend'){S.login.resend=26;renderLayer();return}
 if(k==='lcheck'){var ins=[].slice.call(document.querySelectorAll('[data-code]')),cd=ins.map(function(x){return x.value}).join('');if(cd.length<6||cd==='000000'){S.login.err=true;renderLayer()}else{S.login.step='reg';S.login.err=false;renderLayer()}return}
 if(k==='lfinish'){S.user={};S.profile.fio=S.login.fio;S.profile.email=S.login.email;S.profile.phone=S.login.phone.replace(/[\s-]/g,'');S.login=null;S.step=1;go('new');return}
});
document.addEventListener('keydown',function(e){
 if(e.key==='Escape'&&(S.menu||S.modal||S.sheet||S.login)){S.login=null;S.menu=false;S.modal=null;S.sheet=null;renderLayer()}
 if((e.key==='Enter'||e.key===' ')&&e.target.getAttribute&&e.target.getAttribute('role')==='button'&&e.target.tagName==='DIV'){e.preventDefault();e.target.click()}
 if(e.key==='Backspace'&&e.target.dataset&&e.target.dataset.code!==undefined&&!e.target.value){var i=+e.target.dataset.code,ins=document.querySelectorAll('[data-code]');if(ins[i-1])ins[i-1].focus()}
});
document.addEventListener('input',function(e){
 var t=e.target;
 if(t.dataset.code!==undefined){var i=+t.dataset.code;t.value=t.value.replace(/\D/g,'').slice(0,1);var ins=[].slice.call(document.querySelectorAll('[data-code]'));if(t.value&&ins[i+1])ins[i+1].focus();return}
 var b=t.dataset.bind;if(!b)return;
 if(b==='addr'){S.addr=t.value;var bad=addrBad(),h=$('#ahint');t.parentNode.classList.toggle('bad',bad);if(h){h.textContent=addrHintText();h.classList.toggle('bad',bad)}sync()}
 else if(b==='bq'){S.q=t.value;$('#blist').innerHTML=bankList()}
 else if(b==='lph'){var f=fmtPhone(t.value);t.value=f;S.login.phone=f;$('#lgo').disabled=f.replace(/\D/g,'').length<11}
 else if(b==='lfio'||b==='lem'){S.login[b==='lfio'?'fio':'email']=t.value;$('#lfin').disabled=!regOk(S.login)}
 else if(b==='link'){getOrder(S.openId).link=t.value;sync()}
 else if(b==='pfio'){S.profile.fio=t.value}else if(b==='pemail'){S.profile.email=t.value}
});
document.addEventListener('scroll',function(e){var t=e.target;if(t&&(t.id==='wsl'||t.id==='ssl')){var it=t.children,best=0,bd=1e9;for(var i=0;i<it.length;i++){var d=Math.abs(it[i].offsetLeft-t.offsetLeft-t.scrollLeft-parseFloat(getComputedStyle(t).paddingLeft||0));if(d<bd){bd=d;best=i}}[].forEach.call(document.querySelectorAll(t.id==='ssl'?'.sdots button':'.wdots button'),function(b,j){b.classList.toggle('on',j===best)});return}if(t&&t.id==='scroller'){var n=$('#nav');if(n)n.classList.toggle('solid',t.scrollTop>8)}},true);

function pressed(group,val){[].forEach.call(document.querySelectorAll('[data-demo^="'+group+':"]'),function(b){b.setAttribute('aria-pressed',String(b.getAttribute('data-demo')===group+':'+val))})}
var mq=window.matchMedia?window.matchMedia('(prefers-color-scheme: dark)'):null;
function applyMode(){var t=document.documentElement.getAttribute('data-theme');var dark=t==='dark'||(!t&&mq&&mq.matches);$('#phone').setAttribute('data-mode',dark?'dark':'light')}
if(mq){if(mq.addEventListener)mq.addEventListener('change',applyMode);else if(mq.addListener)mq.addListener(applyMode)}
function setDir(v){$('#phone').setAttribute('data-dir',v);var n=$('#dirnote');if(n)n.textContent=DIRS[v];pressed('dir',v)}
function demo(cmd){
 var p=cmd.split(':'),k=p[0],v=p[1];
 if(k==='panel'){var cl=v==='toggle'?!document.body.classList.contains('clean'):v==='hide';document.body.classList.toggle('clean',cl);var tb=$('#ptoggle');if(tb){tb.textContent=cl?'Показать панель':'Скрыть панель';tb.setAttribute('aria-pressed',String(cl))}try{localStorage.setItem('lz-panel',cl?'hide':'show')}catch(e){}if(typeof fitZoom==='function')fitZoom();return}
 if(k==='dir'){setDir(v);return}
 if(k==='sc'){scenario(v);return}
 if(k==='pal'){$('#phone').setAttribute('data-pal',v);pressed('pal',v);if(v!=='aurora')setDir('a');return}
 if(k==='hero'){$('#phone').setAttribute('data-hero',v);pressed('hero',v);if(S.screen!=='home')demo('go:home');var sc=$('#scroller');if(sc)sc.scrollTop=0;return}
 if(k==='logo'){LOGO=v;pressed('logo',v);render();return}
 if(k==='why'){WHY=v;pressed('why',v);if(S.screen!=='home')demo('go:home');else render();setTimeout(function(){var h=[].filter.call(document.querySelectorAll('h3.sec'),function(x){return /Почему/.test(x.textContent)})[0],sc=$('#scroller');if(h&&sc)sc.scrollTop=h.offsetTop-70},30);return}
 if(k==='tagst'){TAGSTYLE=v;pressed('tagst',v);render();return}
 if(k==='flat'){$('#phone').classList.toggle('flat',v==='on');pressed('flat',v);return}
 if(k==='theme'){var r=document.documentElement;if(v==='auto')r.removeAttribute('data-theme');else r.setAttribute('data-theme',v);pressed('theme',v);applyMode();return}
 if(k==='mode'){S.working=v==='on';pressed('mode',v);if(S.screen==='home')render();return}
 if(k==='speed'){speedKeep=+v;pressed('speed',v);return}
 if(k==='auth'){S.user=v==='in'?{}:null;S.askLogin=v==='ask';pressed('auth',v);return}
 if(k==='reset'){fresh({working:S.working,user:S.askLogin?null:{},askLogin:S.askLogin});render();return}
 if(k==='go'){
  if(v==='new'){if(!S.user)S.user={};S.dir='buy';S.coin='TRX';S.amount=5000;resetReq();go('new')}
  else if(v==='order'){var act=S.orders.filter(function(o){return o.status==='created'||o.status==='pay'})[0]||S.orders[0];S.openId=act.id;go('order')}
  else go(v);
 }
}
applyMode();setDir('a');
render();

(function(){var d=null;
function pl(w){return parseFloat(getComputedStyle(w).paddingLeft||0)}
function pos(w,i){var it=w.children[i];return it.offsetLeft-w.offsetLeft-pl(w)}
document.addEventListener('pointerdown',function(e){var w=e.target.closest&&e.target.closest('#wsl,#ssl');if(!w||e.pointerType==='touch'||e.button!==0)return;d={w:w,x:e.clientX,s:w.scrollLeft,m:false,t:Date.now()}});
document.addEventListener('pointermove',function(e){if(!d)return;var dx=(e.clientX-d.x)/ZM;if(!d.m&&Math.abs(dx)>4){d.m=true;d.w.style.scrollSnapType='none';d.w.classList.add('drag')}if(d.m){d.w.scrollLeft=d.s-dx}});
function end(e){if(!d)return;var w=d.w;if(d.m){var dx=(e.clientX-d.x)/ZM,n=w.children.length,best=0,bd=1e9;for(var i=0;i<n;i++){var dd=Math.abs(pos(w,i)-w.scrollLeft);if(dd<bd){bd=dd;best=i}}
 if(Math.abs(dx)>40&&Math.abs(pos(w,best)-d.s)<8)best=Math.max(0,Math.min(n-1,best+(dx<0?1:-1)));
 w.classList.remove('drag');w.style.scrollSnapType='';w.scrollTo({left:pos(w,best),behavior:'smooth'});d.sup=true;setTimeout(function(){},0)}d=null}
document.addEventListener('pointerup',end);document.addEventListener('pointercancel',end);
document.addEventListener('dragstart',function(e){if(e.target.closest&&e.target.closest('#wsl,#ssl'))e.preventDefault()});
})();

(function(){var g=null;
document.addEventListener('pointerdown',function(e){var h=e.target.closest&&e.target.closest('.sheet .grab');if(!h||e.button!==0)return;var sh=h.closest('.sheet');g={sh:sh,y:e.clientY,t:Date.now(),dy:0};sh.style.animation='none';sh.style.transition='none';try{h.setPointerCapture(e.pointerId)}catch(_){}});
document.addEventListener('pointermove',function(e){if(!g)return;var dy=(e.clientY-g.y)/ZM;g.dy=dy>0?dy:dy/6;g.sh.style.transform='translateY('+g.dy+'px)'});
function up(){if(!g)return;var sh=g.sh,v=g.dy/Math.max(1,Date.now()-g.t);sh.style.transition='transform .45s var(--sp)';if(g.dy>110||v>.6){sh.style.transition='transform .22s ease-in';sh.style.transform='translateY(110%)';var sc=sh.closest('.scrim');setTimeout(function(){if(sc)sc.click()},170)}else{sh.style.transform='none'}g=null}
document.addEventListener('pointerup',up);document.addEventListener('pointercancel',up);
})();
window.addEventListener('resize',function(){alignIcons($('#app'));alignIcons($('#layer'))});
/* в панели только «Светлая» и «Тёмная»: стартуем с темы системы */
demo('theme:'+(mq&&mq.matches?'dark':'light'));
/* крупный интерфейс на больших экранах: масштаб по высоте окна, не выше 1,5 */
function fitZoom(){var W=window.innerWidth,H=window.innerHeight,z=1;if(W>700){z=Math.min(Math.max(H/760,1),1.5,(W-32-(document.body.classList.contains('clean')?0:328))/390);z=Math.max(1,Math.round(z*100)/100)}
 if(z!==ZM){ZM=z;document.documentElement.style.setProperty('--z',String(z));alignIcons($('#app'));alignIcons($('#layer'));fitTree($('#phone'))}}
window.addEventListener('resize',fitZoom);
/* панель: по умолчанию видна; #clean в адресе или прошлый выбор скрывают её */
(function(){var h=/github\.io$/.test(location.hostname),pv=null;try{pv=localStorage.getItem('lz-panel')}catch(e){}if(pv)h=pv==='hide';if(location.hash==='#clean')h=true;if(location.hash==='#panel')h=false;if(h)demo('panel:hide')})();
fitZoom();
})();
</script>
