/* типографика: неразрывные пробелы (предлоги, союзы, частицы, число + единица, тире, тысячи), висячие предлоги, висячее последнее слово.
   Правила те же, что в Figma-проходе; функция идемпотентна */
var NB=' ',TH=' ',NH='‑';
var PREP='в|во|к|ко|с|со|у|о|об|обо|от|до|на|по|за|из|не|ни|но|да|для|при|без|над|под|про|или|что|как|а|и|я|чем|то|же|ли|бы';
var RX_SHORT=new RegExp('(^|[ '+NB+'(«„"—–])('+PREP+') ','gi');
var RX_SP=new RegExp('[ '+NB+']');
function typo(s,last){if(!s||s.length<2)return s;
 s=s.replace(/\.\.\./g,'…');
 s=s.replace(new RegExp('[ '+NB+']+[-–—][ '+NB+']+','g'),NB+'— ');
 s=s.replace(/(\S) {2,}(?=\S)/g,'$1 ');
 var phone=/\+\d|\d{2}-\d{2}(?!\d)/.test(s);
 s=s.replace(RX_SHORT,function(m,a,w){return a+w+NB}).replace(RX_SHORT,function(m,a,w){return a+w+NB});
 s=s.replace(/(\S) (же|ли|бы)(?=[ .,;:!?)»]|$)/gi,'$1'+NB+'$2');
 s=s.replace(new RegExp('(\\d)[ '+NB+TH+'](?=\\d{3}(?!\\d))','g'),'$1'+(phone?NB:TH));
 s=s.replace(/(\d) (?=[A-Za-zА-Яа-яЁё₽$€%°₿])/g,'$1'+NB);
 s=s.replace(/([A-Za-zА-Яа-яЁё]) (?=[$€₽]\d)/g,'$1'+NB);
 s=s.replace(/([№§]) /g,'$1'+NB).replace(/ = /g,NB+'='+NB).replace(/ · /g,NB+'· ');
 s=s.replace(/(^|[^А-Яа-яЁёA-Za-z])([ТтA-Z])-(?=[А-ЯЁA-Z])/g,'$1$2'+NH);
 if(last&&s.split(RX_SP).length>=5){var i=Math.max(s.lastIndexOf(' '),s.lastIndexOf(NB));if(i>0&&s.charAt(i)===' '){var l=s.slice(i+1),pv=s.slice(0,i).split(RX_SP).pop();if(l.length<=12&&l.length+pv.length<=18)s=s.slice(0,i)+NB+l}}
 return s}
function typoOk(n){var p=n.parentNode;return !!p&&!/^(SCRIPT|STYLE|TEXTAREA|CODE|INPUT|TITLE)$/.test(p.nodeName)&&!(p.closest&&p.closest('.mono,[data-notypo]'))}
function typoNode(n){if(n.nodeValue.trim().length<2||!typoOk(n))return;var v=typo(n.nodeValue,!n.nextSibling);if(v!==n.nodeValue)n.nodeValue=v}
function typoTree(root){if(!root)return;if(root.nodeType===3){typoNode(root);return}var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),n,list=[];while((n=w.nextNode()))list.push(n);list.forEach(typoNode)}
/* типограф следит за DOM: любой новый или изменённый текст (подсказки, таймеры, тосты) обрабатывается сразу */
(function(){var q=[],f=0;function run(){f=0;var a=q;q=[];a.forEach(typoTree)}
 new MutationObserver(function(ms){ms.forEach(function(m){if(m.type==='characterData')q.push(m.target);else[].forEach.call(m.addedNodes,function(n){q.push(n)})});if(!f){f=1;requestAnimationFrame(run)}}).observe(document.body,{childList:true,subtree:true,characterData:true});
 document.addEventListener('DOMContentLoaded',function(){typoTree(document.body)})})();
