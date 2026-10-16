(ICONS)=>{
const ICMAP={};{const tmp=document.createElementNS('http://www.w3.org/2000/svg','svg');for(const k in ICONS){tmp.innerHTML=ICONS[k];ICMAP[tmp.innerHTML.replace(/\s+/g,' ').trim()]=k}}
const phone=document.querySelector('.phone');const PR=phone.getBoundingClientRect();
const INLINE=new Set(['inline']);
const px=v=>{const n=parseFloat(v);return isNaN(n)?0:Math.round(n*100)/100};
function vis(el){const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden')return false;if(parseFloat(s.opacity)===0)return false;return true}
function shadows(s){const v=s.boxShadow;if(!v||v==='none')return [];const parts=[];let d=0,cur='';for(const ch of v){if(ch==='(')d++;if(ch===')')d--;if(ch===','&&d===0){parts.push(cur.trim());cur=''}else cur+=ch}if(cur.trim())parts.push(cur.trim());
 return parts.map(p=>{const inset=/inset/.test(p);p=p.replace('inset','').trim();const m=p.match(/^(rgba?\([^)]*\)|color\([^)]*\)|#[0-9a-f]+)\s+(.*)$/i);let col,rest;if(m){col=m[1];rest=m[2]}else{const m2=p.match(/^(.*?)\s+(rgba?\([^)]*\)|color\([^)]*\))$/);col=m2?m2[2]:'rgba(0,0,0,0)';rest=m2?m2[1]:p}const n=rest.trim().split(/\s+/).map(px);return {c:col,x:n[0]||0,y:n[1]||0,b:n[2]||0,s:n[3]||0,i:inset}})}
function radius(s,w,h){const f=v=>{if(String(v).includes('%'))return Math.min(w,h)*parseFloat(v)/100;return px(v)};const r=[f(s.borderTopLeftRadius),f(s.borderTopRightRadius),f(s.borderBottomRightRadius),f(s.borderBottomLeftRadius)].map(x=>Math.min(x,Math.min(w,h)/2));if(r.every(x=>x===0))return undefined;if(r.every(x=>x===r[0]))return r[0];return r}
function borders(s){const o={};for(const [k,n] of [['t','Top'],['r','Right'],['b','Bottom'],['l','Left']]){const w=px(s['border'+n+'Width']);const st=s['border'+n+'Style'];const c=s['border'+n+'Color'];if(w>0&&st!=='none'&&!/rgba\(\s*0,\s*0,\s*0,\s*0\)/.test(c)&&c!=='transparent')o[k]=[w,c]}return Object.keys(o).length?o:undefined}
function fontKey(s){return [s.fontFamily.split(',')[0].replace(/['"]/g,'').trim(),s.fontWeight,px(s.fontSize),s.lineHeight==='normal'?'n':px(s.lineHeight),s.letterSpacing==='normal'?0:px(s.letterSpacing),s.textTransform==='uppercase'?'U':'',s.textDecorationLine&&s.textDecorationLine.includes('underline')?'u':''].join('|')}
function txtColor(el,s){if(s.webkitTextFillColor&&/rgba\(0, 0, 0, 0\)/.test(s.webkitTextFillColor)||(/rgba\(0, 0, 0, 0\)/.test(s.color)&&s.backgroundImage!=='none'))return 'G:'+s.backgroundImage;return s.color}
function isTexty(el){let hasText=false;for(const n of el.childNodes){if(n.nodeType===3){if(n.nodeValue.trim())hasText=true}else if(n.nodeType===1){if(!vis(n))continue;const s=getComputedStyle(n);if(n.tagName.toLowerCase()==='svg'||n.tagName==='INPUT')return false;if(!INLINE.has(s.display)&&n.tagName!=='BR')return false;if(s.backgroundColor!=='rgba(0, 0, 0, 0)'||s.position==='absolute')return false;if(n.querySelector('svg,input'))return false}}return hasText||!!el.querySelector('br')&&el.textContent.trim()}
function runs(el,olIdx){const out=[];const walk=(n,inh)=>{for(const c of n.childNodes){if(c.nodeType===3){let t=c.nodeValue.replace(/[ \t\n\r\f]+/g,' ');if(!t)continue;const p=c.parentElement,s=getComputedStyle(p);out.push({t,f:fontKey(s),c:txtColor(p,s)})}else if(c.nodeType===1&&vis(c)){if(c.tagName==='BR'){out.push({t:'\n',f:out.length?out[out.length-1].f:fontKey(getComputedStyle(n)),c:out.length?out[out.length-1].c:getComputedStyle(n).color});continue}walk(c)}}};walk(el);
 if(olIdx){const s=getComputedStyle(el);out.unshift({t:olIdx+'. ',f:fontKey(s),c:s.color})}
 // trim
 while(out.length&&!out[0].t.trim()&&out[0].t!=='\n')out.shift();if(out.length)out[0].t=out[0].t.replace(/^ +/,'');while(out.length&&!out[out.length-1].t.trim())out.pop();if(out.length)out[out.length-1].t=out[out.length-1].t.replace(/ +$/,'');
 for(let i=0;i<out.length;i++){out[i].t=out[i].t.replace(/ ?\n ?/g,'\n')}
 // merge
 const m=[];for(const r of out){const l=m[m.length-1];if(l&&l.f===r.f&&l.c===r.c)l.t+=r.t;else m.push({...r})}return m}
function nlines(el){const rg=document.createRange();rg.selectNodeContents(el);const tops=new Set();for(const r of rg.getClientRects()){if(r.width>0.5)tops.add(Math.round(r.top+r.height/2))}let n=0,prev=null;for(const t of [...tops].sort((a,b)=>a-b)){if(prev===null||t-prev>4)n++;prev=t}return n}
function lh(s){return s.lineHeight==='normal'?px(s.fontSize)*1.22:px(s.lineHeight)}
function base(el,s,r,pr){const o={x:Math.round((r.x-pr.x)*10)/10,y:Math.round((r.y-pr.y)*10)/10,w:Math.round(r.width*10)/10,h:Math.round(r.height*10)/10,ax:Math.round(r.x-PR.x-1),ay:Math.round(r.y-PR.y-1)};
 const cls0=(typeof el.className==='string'?el.className:(el.className&&el.className.baseVal)||'').trim();const cls=cls0;if(cls)o.cls=cls;o.tag=el.tagName.toLowerCase();
 if(s.position==='absolute'||s.position==='fixed')o.abs=1;
 const g=parseFloat(s.flexGrow);if(g>0)o.grow=g;if(s.alignSelf&&s.alignSelf!=='auto'&&s.alignSelf!=='normal')o.as=s.alignSelf;
 if(s.minHeight&&s.minHeight!=='auto'&&px(s.minHeight)>0)o.minH=px(s.minHeight);
 if(parseFloat(s.opacity)<1)o.op=parseFloat(s.opacity);
 for(const a of ['aria-pressed','aria-selected','aria-current'])if(el.getAttribute&&el.getAttribute(a))o[a.replace('aria-','')]=el.getAttribute(a);
 if(el.disabled)o.dis=1;
 const tf=s.transform;if(tf&&tf!=='none'){const m=tf.match(/matrix\(([^)]*)\)/);if(m){const v=m[1].split(',').map(parseFloat);const ang=Math.round(Math.atan2(v[1],v[0])*180/Math.PI);if(ang)o.rot=ang}}
 return o}
function box(o,s,el){if(s.backgroundColor!=='rgba(0, 0, 0, 0)')o.bg=s.backgroundColor;if(s.backgroundImage!=='none'&&!(s.webkitBackgroundClip==='text'||s.backgroundClip==='text'))o.bgi=s.backgroundImage;const r=radius(s,o.w,o.h);if(r!==undefined)o.r=r;const sh=shadows(s);if(sh.length)o.sh=sh;const b=borders(s);if(b)o.bd=b;if(['auto','scroll','hidden'].includes(s.overflowX)&&el.scrollWidth>el.clientWidth+2)o.clipx=1;if(['auto','scroll','hidden'].includes(s.overflowY)&&el.scrollHeight>el.clientHeight+2)o.clipy=1;return o}
function layout(o,el,s){const d=s.display;const bw=[px(s.borderTopWidth),px(s.borderRightWidth),px(s.borderBottomWidth),px(s.borderLeftWidth)].map((v,i)=>[s.borderTopStyle,s.borderRightStyle,s.borderBottomStyle,s.borderLeftStyle][i]==='none'?0:v);const pad=[px(s.paddingTop)+bw[0],px(s.paddingRight)+bw[1],px(s.paddingBottom)+bw[2],px(s.paddingLeft)+bw[3]];if(pad.some(x=>x))o.pad=pad;
 if(d.includes('flex')){o.L=s.flexDirection.startsWith('column')?'V':'H';o.gap=px(s.columnGap==='normal'?0:(o.L==='H'?s.columnGap:s.rowGap));if(o.L==='V')o.gap=px(s.rowGap==='normal'?0:s.rowGap);o.ai=s.alignItems;o.jc=s.justifyContent;if(s.flexWrap==='wrap'){o.wrap=1;o.rgap=px(s.rowGap==='normal'?0:s.rowGap)}}
 else if(d.includes('grid')){const cols=s.gridTemplateColumns&&s.gridTemplateColumns!=='none'?s.gridTemplateColumns.split(/\s+(?![^(]*\))/).length:1;o.L='G';o.cols=cols;o.gap=px(s.columnGap==='normal'?0:s.columnGap);o.rgap=px(s.rowGap==='normal'?0:s.rowGap);o.ai=s.alignItems;o.jc=s.justifyContent;o.ji=s.justifyItems;}
 else{o.L='B'}
 o.ta=s.textAlign}
function X(el,pr,ctx){if(!vis(el))return null;if(el.classList&&(el.classList.contains('demo')||el.id==='toast'))return null;const s=getComputedStyle(el);const r=el.getBoundingClientRect();if(r.width<0.5&&r.height<0.5&&!el.querySelector('*'))return null;
 const tag=el.tagName.toLowerCase();let o=base(el,s,r,pr);
 if(tag==='svg'){const inner=el.innerHTML.replace(/\s+/g,' ').trim();const k=ICMAP[inner];o.col=s.color;if(k){o.t='i';o.k=k;return o}o.t='g';let h=el.outerHTML.replace(/currentColor/g,s.color);h=h.replace(/var\(--([a-z0-9-]+)\)/g,(m,v)=>getComputedStyle(el).getPropertyValue('--'+v).trim()||m);o.svg=h;return o}
 if(el.classList.contains('ring')){o.t='ring';const c=el.querySelectorAll('circle');o.da=c[1].getAttribute('stroke-dasharray');o.rc=getComputedStyle(c[1]).stroke;o.tc=getComputedStyle(c[0]).stroke;const b=el.querySelector('b');o.lbl={t:b.textContent,f:fontKey(getComputedStyle(b)),c:getComputedStyle(b).color};return o}
 if(el.classList.contains('spin')){o.t='spin';o.c1=s.borderTopColor;o.c2=s.borderRightColor;o.bw=px(s.borderTopWidth);return o}
 if(tag==='input'){const ty=el.type;if(ty==='checkbox'){box(o,s,el);o.t=el.classList.contains('sw')?'sw':'cb';o.on=el.checked?1:0;const bf=getComputedStyle(el,'::before');o.knob={bg:bf.backgroundColor,w:px(bf.width),h:px(bf.height),sh:shadows(bf)};const af=getComputedStyle(el,'::after');if(af.content&&af.content!=='none'){o.mark={c:af.borderColor||af.color,bg:af.backgroundColor}}return o}
  if(s.backgroundColor!=='rgba(0, 0, 0, 0)'||px(s.borderTopWidth)>0&&s.borderTopStyle!=='none'||s.boxShadow!=='none'){box(o,s,el);o.t='f';o.L='V';o.ai='center';o.jc='center';o.ta='center';const v2=el.value;const ps2=getComputedStyle(el,'::placeholder');o.ch=[{t:'x',runs:[{t:v2||el.placeholder||' ',f:fontKey(s),c:v2?s.color:ps2.color}],x:0,y:0,w:o.w,h:o.h,wrap:0,ta:s.textAlign}];o.pad=[px(s.paddingTop),px(s.paddingRight),px(s.paddingBottom),px(s.paddingLeft)];return o}
  o.t='x';const v=el.value;const ps=getComputedStyle(el,'::placeholder');const txt=v||el.placeholder||'';o.runs=[{t:txt,f:fontKey(s),c:v?s.color:ps.color}];o.wrap=0;if(s.textOverflow==='ellipsis'||el.scrollWidth>el.clientWidth+1)o.trunc=1;o.ta=s.textAlign;o.grow=parseFloat(s.flexGrow)||1;return o}
 box(o,s,el);layout(o,el,s);
 const olIdx=ctx&&ctx.olIdx;
 if(isTexty(el)){const rs=runs(el,olIdx);if(rs.length){const ps=getComputedStyle(el,'::after');const dot=(ps.content&&ps.content!=='none'&&ps.position==='static'&&px(ps.width)>0&&ps.backgroundColor!=='rgba(0, 0, 0, 0)')?{t:'f',cls:'dot',tag:'i',w:px(ps.width),h:px(ps.height),bg:ps.backgroundColor,r:px(ps.width)/2,L:'B',x:0,y:0}:null;const boxy=dot||o.bg||o.bgi||o.pad||o.sh||o.bd||(o.L!=='B'&&o.L);o.t=boxy?'f':'x';const _rg=document.createRange();_rg.selectNodeContents(el);const _rb=_rg.getBoundingClientRect();const tn={t:'x',runs:rs,x:0,y:0,w:o.w-(o.pad?o.pad[1]+o.pad[3]:0),h:o.h-(o.pad?o.pad[0]+o.pad[2]:0),ta:s.textAlign,tw:Math.round(_rb.width*10)/10,th:Math.round(_rb.height*10)/10};tn.wrap=nlines(el)>1?1:0;if(dot){o.L='H';o.ai='center';o.gap=px(ps.marginLeft);o.jc='normal';tn.w=tn.w-dot.w-o.gap;o.ch=[tn,dot];if(!o.pad)delete o.pad;return o}if(s.whiteSpace==='nowrap'&&(el.scrollWidth>el.clientWidth+1))tn.trunc=1;
   if(o.t==='x'){Object.assign(o,{runs:rs,wrap:tn.wrap,trunc:tn.trunc,disp:s.display});return o}
   if(o.pad){tn.x=o.pad[3];tn.y=o.pad[0]}o.ch=[tn];if(!o.L||o.L==='B')o.L='V';return o}}
 o.t='f';const ch=[];let li=0;
 for(const n of el.childNodes){if(n.nodeType===3){const t=n.nodeValue.replace(/[ \t\n\r\f]+/g,' ').replace(/^[ ]+|[ ]+$/g,'');if(!t)continue;const rg=document.createRange();rg.selectNodeContents(n);const rr=rg.getBoundingClientRect();ch.push({t:'x',runs:[{t,f:fontKey(s),c:txtColor(el,s)}],x:Math.round(rr.x-r.x),y:Math.round(rr.y-r.y),w:Math.round(rr.width),h:Math.round(rr.height),wrap:(()=>{const tops=new Set();for(const q of rg.getClientRects())if(q.width>0.5)tops.add(Math.round(q.top));return tops.size>1?1:0})(),anon:1})}
  else if(n.nodeType===1){if(n.tagName==='LI')li++;const c=X(n,r,{olIdx:(tag==='ol'&&n.tagName==='LI')?li:0});if(c)ch.push(c)}}
 // pseudo before/after with content text (badges etc.)
 if(ch.length)o.ch=ch;return o}
const root=X(phone,PR,{});
const layer=document.querySelector('#layer');
return root}
