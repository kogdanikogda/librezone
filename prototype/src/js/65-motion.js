/* ---------- переходы калькулятора: смена направления, выбор суммы, смена монеты ---------- */
var MOTION='live';
var MO={soft:{d:320,e:'cubic-bezier(.2,.8,.2,1)',pop:1.02,n:420},live:{d:620,e:'cubic-bezier(.34,1.56,.64,1)',pop:1.07,n:640}};
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
  var m=/[,.](\d+)\s*$/.exec(to),dec=m?m[1].length:0,t0=performance.now();
  (function f(t){var p=Math.min(1,(t-t0)/c.n),q=1-Math.pow(1-p,3);el.textContent=p>=1?to:nf(a+(b-a)*q,dec);if(p<1)requestAnimationFrame(f)})(t0)})}
/* смена направления: строки обмениваются местами, кнопка поворачивается */
function moSwap(sn){if(!moOn()||!sn)return;var c=moCfg(),rows=document.querySelectorAll('#app .pairbox .crow');if(rows.length<2||sn.tops.length<2)return;
 var dy=sn.tops[1]-sn.tops[0];
 [rows[0],rows[1]].forEach(function(r,i){var s=i===0?1:-1;
  [].forEach.call(r.querySelectorAll('.amt,.curpill'),function(el){moAnim(el,[{transform:'translateY('+s*dy+'px)',opacity:.15},{opacity:1,offset:.45},{transform:'translateY(0)',opacity:1}],{duration:c.d,easing:c.e})})});
 var sb=document.querySelector('.swapbtn');if(sb){sb.style.animationDuration=c.d+'ms'}}
/* выбор суммы: плитка «переезжает», время обмена выезжает снизу, кнопка оживает */
function moChip(sn){if(!moOn()||!sn)return;var c=moCfg(),chips=[].slice.call(document.querySelectorAll('#app .chip')),ni=CHIPS.indexOf(S.amount);
 if(sn.idx>=0&&chips[sn.idx])chips[sn.idx].setAttribute('aria-pressed','true');
 if(chips[ni])chips[ni].setAttribute('aria-pressed','false');
 void document.body.offsetWidth;
 if(sn.idx>=0&&chips[sn.idx])chips[sn.idx].setAttribute('aria-pressed','false');
 if(chips[ni]){chips[ni].setAttribute('aria-pressed','true');moAnim(chips[ni],[{transform:'scale(.9)'},{transform:'scale('+c.pop+')',offset:.55},{transform:'scale(1)'}],{duration:c.d,easing:'ease-out'})}
 var eta=document.querySelector('#app .eta');moAnim(eta,[{opacity:0,transform:'translateY(10px)'},{opacity:1,transform:'none'}],{duration:c.d,easing:c.e});
 if(sn.idx<0){var b=document.querySelector('#app .calcbtn');moAnim(b,[{opacity:.5,transform:'scale(.96)'},{opacity:1,transform:'scale('+c.pop+')',offset:.6},{opacity:1,transform:'none'}],{duration:c.d,easing:c.e})}
 moCount(sn)}
