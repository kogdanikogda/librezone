/* ---------- переходы калькулятора: смена направления, выбор суммы, смена монеты ---------- */
var MOTION='live';
var MO={soft:{d:260,e:'cubic-bezier(.2,.8,.2,1)',live:0,n:380},live:{d:760,e:'cubic-bezier(.3,1.7,.5,1)',live:1,n:900}};
function moOn(){return MOTION!=='off'&&!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches)}
function moCfg(){return MO[MOTION]||MO.soft}
function moAnim(el,kf,o){if(el&&el.animate)try{el.animate(kf,o)}catch(e){}}
function moNum(t){var v=parseFloat(String(t).replace(/[\s  ]/g,'').replace(',','.'));return isNaN(v)?0:v}
/* снимок до перерисовки: позиции строк, тексты сумм, выбранная плитка */
function moSnap(){var rows=[].slice.call(document.querySelectorAll('#app .pairbox .crow')),am=[].slice.call(document.querySelectorAll('#app .pairbox .amt'));
 return {tops:rows.map(function(r){return r.getBoundingClientRect().top}),ghosts:rows.map(function(r){var g=r.cloneNode(true),b=r.getBoundingClientRect();[].forEach.call(g.querySelectorAll('.lbl'),function(l){l.style.visibility='hidden'});return {el:g,top:b.top,left:b.left,w:b.width,h:b.height}}),txt:am.map(function(a){return a.textContent}),idx:CHIPS.indexOf(S.amount)}}
/* суммы плавно «досчитываются» от прошлого значения к новому */
function moCount(sn){if(!moOn()||!sn)return;var c=moCfg();
 [].forEach.call(document.querySelectorAll('#app .pairbox .amt'),function(el,i){
  var to=el.textContent,a=moNum(sn.txt[i]),b=moNum(to);if(sn.txt[i]===undefined||a===b)return;
  if(c.live)moAnim(el,[{transform:'scale(1)'},{transform:'scale(1.12)',offset:.3},{transform:'scale(1)'}],{duration:c.n,easing:'ease-out'});
  var m=/[,.](\d+)\s*$/.exec(to),dec=m?m[1].length:0,t0=performance.now();
  (function f(t){var p=Math.min(1,(t-t0)/c.n),q=1-Math.pow(1-p,3);el.textContent=p>=1?to:nf(Math.max(0,a+(b-a)*q),dec);if(p<1)requestAnimationFrame(f)})(t0)})}
/* смена направления: строки обмениваются местами, кнопка поворачивается */
function moSwap(sn){if(!moOn()||!sn)return;var c=moCfg(),pb=document.querySelector('#app .pairbox'),rows=document.querySelectorAll('#app .pairbox .crow'),sb=document.querySelector('.swapbtn');if(!pb||rows.length<2)return;
 if(c.live){
  /* старые строки уходят с небольшим уменьшением, новые появляются в другой позиции с лёгким увеличением */
  var pr=pb.getBoundingClientRect(),z=ZM||1;if(getComputedStyle(pb).position==='static')pb.style.position='relative';
  (sn.ghosts||[]).forEach(function(g){var e=g.el;e.style.cssText+=';position:absolute;pointer-events:none;margin:0;left:'+((g.left-pr.left)/z)+'px;top:'+((g.top-pr.top)/z)+'px;width:'+(g.w/z)+'px;height:'+(g.h/z)+'px';
   e.setAttribute('data-g','1');pb.appendChild(e);var an=e.animate([{opacity:1,transform:'scale(1)'},{opacity:0,transform:'scale(.9)'}],{duration:180,easing:'ease-in',fill:'forwards'});an.onfinish=function(){e.remove()}});
  [].forEach.call(pb.querySelectorAll('.crow:not(.ghost) .amt,.crow:not(.ghost) .curpill'),function(el){if(el.closest('[data-g]'))return;moAnim(el,[{opacity:0,transform:'scale(.88)'},{opacity:1,transform:'scale(1)'}],{duration:340,delay:150,easing:'cubic-bezier(.34,1.3,.64,1)',fill:'backwards'})});
  if(sb)moAnim(sb,[{transform:'rotate(0)'},{transform:'rotate(180deg)'}],{duration:420,easing:'cubic-bezier(.4,0,.2,1)'});
 }else{
  [].forEach.call(rows,function(r,i){[].forEach.call(r.querySelectorAll('.amt,.curpill'),function(el){moAnim(el,[{transform:'translateY('+(i===0?10:-10)+'px)',opacity:0},{transform:'translateY(0)',opacity:1}],{duration:c.d,easing:c.e,fill:'backwards'})})});
  if(sb)moAnim(sb,[{transform:'rotate(-90deg)',opacity:.5},{transform:'none',opacity:1}],{duration:c.d,easing:c.e})}
 if(sb)sb.classList.remove('rot')}
/* выбор суммы: плитка «переезжает», время обмена выезжает снизу, кнопка оживает */
function moChip(sn){if(!moOn()||!sn)return;var c=moCfg(),chips=[].slice.call(document.querySelectorAll('#app .chip')),ni=CHIPS.indexOf(S.amount);
 if(sn.idx>=0&&chips[sn.idx])chips[sn.idx].setAttribute('aria-pressed','true');
 if(chips[ni])chips[ni].setAttribute('aria-pressed','false');
 void document.body.offsetWidth;
 if(sn.idx>=0&&chips[sn.idx])chips[sn.idx].setAttribute('aria-pressed','false');
 if(chips[ni]){chips[ni].setAttribute('aria-pressed','true');
  if(c.live)moAnim(chips[ni],[{transform:'scale(.82)'},{transform:'scale(1.14) rotate(-2deg)',offset:.4},{transform:'scale(.97) rotate(1deg)',offset:.7},{transform:'scale(1)'}],{duration:c.d,easing:'ease-out'});
  if(c.live&&sn.idx>=0&&chips[sn.idx])moAnim(chips[sn.idx],[{transform:'scale(.9)'},{transform:'scale(1)'}],{duration:c.d,easing:c.e})}
 var eta=document.querySelector('#app .eta');if(eta)[].forEach.call(eta.children,function(k){moAnim(k,[{opacity:0},{opacity:1}],{duration:c.live?420:c.d,easing:'ease-out'})});
 if(sn.idx<0){var b=document.querySelector('#app .calcbtn');if(c.live)moAnim(b,[{opacity:.4,transform:'scale(.9)'},{opacity:1,transform:'scale(1.06)',offset:.55},{opacity:1,transform:'none'}],{duration:c.d,easing:c.e});else moAnim(b,[{opacity:.5},{opacity:1}],{duration:c.d,easing:c.e})}
 moCount(sn)}
