/* ---------- переходы калькулятора: смена направления, выбор суммы, смена монеты ---------- */
var MOTION='live';
var MO={soft:{d:260,e:'cubic-bezier(.2,.8,.2,1)',live:0,n:380},live:{d:760,e:'cubic-bezier(.3,1.7,.5,1)',live:1,n:900}};
function moOn(){return MOTION!=='off'&&!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches)}
function moCfg(){return MO[MOTION]||MO.soft}
function moAnim(el,kf,o){if(el&&el.animate)try{el.animate(kf,o)}catch(e){}}
function moNum(t){var v=parseFloat(String(t).replace(/[\s  ]/g,'').replace(',','.'));return isNaN(v)?0:v}
/* снимок до перерисовки: позиции строк, тексты сумм, выбранная плитка */
function moSnap(){var rows=[].slice.call(document.querySelectorAll('#app .pairbox .crow')),am=[].slice.call(document.querySelectorAll('#app .pairbox .amt'));
 return {tops:rows.map(function(r){return r.getBoundingClientRect().top}),txt:am.map(function(a){return a.textContent}),idx:CHIPS.indexOf(S.amount)}}
/* суммы плавно «досчитываются» от прошлого значения к новому */
function moCount(sn){if(!moOn()||!sn)return;var c=moCfg();
 [].forEach.call(document.querySelectorAll('#app .pairbox .amt'),function(el,i){
  var to=el.textContent,a=moNum(sn.txt[i]),b=moNum(to);if(sn.txt[i]===undefined||a===b)return;
  if(c.live)moAnim(el,[{transform:'scale(1)'},{transform:'scale(1.12)',offset:.3},{transform:'scale(1)'}],{duration:c.n,easing:'ease-out'});
  var m=/[,.](\d+)\s*$/.exec(to),dec=m?m[1].length:0,t0=performance.now();
  (function f(t){var p=Math.min(1,(t-t0)/c.n),q=c.live?(1+2.70158*Math.pow(p-1,3)+1.70158*Math.pow(p-1,2)):1-Math.pow(1-p,3);el.textContent=p>=1?to:nf(a+(b-a)*q,dec);if(p<1)requestAnimationFrame(f)})(t0)})}
/* смена направления: строки обмениваются местами, кнопка поворачивается */
function moSwap(sn){if(!moOn()||!sn)return;var c=moCfg(),rows=document.querySelectorAll('#app .pairbox .crow');if(rows.length<2||sn.tops.length<2)return;
 var dy=sn.tops[1]-sn.tops[0],sb=document.querySelector('.swapbtn');
 [rows[0],rows[1]].forEach(function(r,i){var s=i===0?1:-1;
  [].forEach.call(r.querySelectorAll('.amt,.curpill'),function(el,j){
   if(c.live)moAnim(el,[{transform:'translateY('+s*dy+'px) scale(.85)',opacity:.1},{opacity:1,offset:.4},{transform:'translateY(0) scale(1)',opacity:1}],{duration:c.d,easing:c.e,delay:j*70,fill:'backwards'});
   else moAnim(el,[{transform:'translateY('+s*10+'px)',opacity:0},{transform:'translateY(0)',opacity:1}],{duration:c.d,easing:c.e,fill:'backwards'})})});
 if(sb){sb.classList.remove('rot');if(c.live)moAnim(sb,[{transform:'rotate(0) scale(1)'},{transform:'rotate(200deg) scale(1.25)',offset:.45},{transform:'rotate(360deg) scale(1)'}],{duration:c.d,easing:'cubic-bezier(.3,1.4,.5,1)'});else moAnim(sb,[{transform:'rotate(-90deg)',opacity:.5},{transform:'none',opacity:1}],{duration:c.d,easing:c.e})}}
/* выбор суммы: плитка «переезжает», время обмена выезжает снизу, кнопка оживает */
function moChip(sn){if(!moOn()||!sn)return;var c=moCfg(),chips=[].slice.call(document.querySelectorAll('#app .chip')),ni=CHIPS.indexOf(S.amount);
 if(sn.idx>=0&&chips[sn.idx])chips[sn.idx].setAttribute('aria-pressed','true');
 if(chips[ni])chips[ni].setAttribute('aria-pressed','false');
 void document.body.offsetWidth;
 if(sn.idx>=0&&chips[sn.idx])chips[sn.idx].setAttribute('aria-pressed','false');
 if(chips[ni]){chips[ni].setAttribute('aria-pressed','true');
  if(c.live)moAnim(chips[ni],[{transform:'scale(.82)'},{transform:'scale(1.14) rotate(-2deg)',offset:.4},{transform:'scale(.97) rotate(1deg)',offset:.7},{transform:'scale(1)'}],{duration:c.d,easing:'ease-out'});
  if(c.live&&sn.idx>=0&&chips[sn.idx])moAnim(chips[sn.idx],[{transform:'scale(.9)'},{transform:'scale(1)'}],{duration:c.d,easing:c.e})}
 var eta=document.querySelector('#app .eta');
 if(c.live)moAnim(eta,[{opacity:0,transform:'translateY(28px) scale(.94)'},{opacity:1,transform:'none'}],{duration:c.d,easing:c.e});else moAnim(eta,[{opacity:0},{opacity:1}],{duration:c.d,easing:c.e});
 if(sn.idx<0){var b=document.querySelector('#app .calcbtn');if(c.live)moAnim(b,[{opacity:.4,transform:'scale(.9)'},{opacity:1,transform:'scale(1.06)',offset:.55},{opacity:1,transform:'none'}],{duration:c.d,easing:c.e});else moAnim(b,[{opacity:.5},{opacity:1}],{duration:c.d,easing:c.e})}
 moCount(sn)}
