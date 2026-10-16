const NS='lzone';
for(const [f,s] of [['Inter','Regular'],['Inter','Medium'],['Inter','Semi Bold'],['Inter','Bold'],['Manrope','SemiBold'],['Manrope','Bold'],['Manrope','ExtraBold']])await figma.loadFontAsync({family:f,style:s});
const V={};(await figma.variables.getLocalVariablesAsync()).forEach(v=>V[v.name]=v);
const TS={};(await figma.getLocalTextStylesAsync()).forEach(s=>TS[s.name]=s);
const ES={};(await figma.getLocalEffectStylesAsync()).forEach(s=>ES[s.name]=s);
const pages={};figma.root.children.forEach(p=>pages[p.name]=p);
await pages.Icons.loadAsync();await pages.Components.loadAsync();
const ICON={};pages.Icons.findAllWithCriteria({types:['COMPONENT']}).forEach(c=>{ICON[c.name.replace('Icon/','')]=c});
const REG={},GREG={};
pages.Components.findAllWithCriteria({types:['COMPONENT']}).forEach(c=>{const k=c.getSharedPluginData(NS,'ck');if(k)REG[k]=c;const g=c.getSharedPluginData(NS,'gk');if(g)GREG[g]=c});
function stage(name){let s=pages.Components.children.find(n=>n.name===name);if(!s){s=figma.createFrame();s.name=name;s.layoutMode='HORIZONTAL';s.layoutWrap='WRAP';s.itemSpacing=40;s.counterAxisSpacing=40;s.paddingLeft=s.paddingRight=s.paddingTop=s.paddingBottom=40;s.primaryAxisSizingMode='FIXED';s.counterAxisSizingMode='AUTO';s.resize(2400,100);s.fills=[];s.clipsContent=false;pages.Components.appendChild(s);const maxY=Math.max(0,...pages.Components.children.filter(x=>x!==s).map(x=>x.y+x.height));s.x=0;s.y=maxY+200}return s}
const COLOR=n=>{const v=V[n];if(!v)throw new Error('no var '+n);return v};
const solid=n=>{const v=COLOR(n);const x=v.valuesByMode[Object.keys(v.valuesByMode)[0]];const c=(x&&x.r!==undefined)?{r:x.r,g:x.g,b:x.b}:{r:0,g:0,b:0};return figma.variables.setBoundVariableForPaint({type:'SOLID',color:c},'color',v)};
function inv(m){const [[a,b,c],[d,e,f]]=m;const det=a*e-b*d;return [[e/det,-b/det,(b*f-c*e)/det],[-d/det,a/det,(c*d-a*f)/det]]}
function gT(deg,w,h){w=w||100;h=h||100;const a=deg*Math.PI/180;const dx=Math.sin(a),dy=-Math.cos(a);const Lp=Math.abs(w*dx)+Math.abs(h*dy);const sx=(w/2-dx*Lp/2)/w,sy=(h/2-dy*Lp/2)/h,ex=(w/2+dx*Lp/2)/w,ey=(h/2+dy*Lp/2)/h;const ux=ex-sx,uy=ey-sy;const px=-uy*(h/w),py=ux*(w/h);const M=[[ux,px,sx-px*0.5],[uy,py,sy-py*0.5]];return inv(M)}
function stop(pos,name,alpha){return {position:pos,color:{r:0,g:0,b:0,a:1},boundVariables:{color:{type:'VARIABLE_ALIAS',id:COLOR(name).id}}}}
function grad(spec,w,h){const g=spec.g;
 if(g==='brand')return {type:'GRADIENT_LINEAR',gradientTransform:gT(150,w,h),gradientStops:[stop(0,'brand/gradient-start'),stop(0.55,'brand/gradient-mid'),stop(1,'brand/gradient-end')]};
 if(g==='hero-text')return {type:'GRADIENT_LINEAR',gradientTransform:gT(150,w,h),gradientStops:[stop(0,'hero/text-start'),stop(0.55,'hero/text-mid'),stop(1,'hero/text-end')]};
 if(g==='hero')return {type:'GRADIENT_LINEAR',gradientTransform:gT(180,w,h),gradientStops:[stop(0,'hero/bg-start'),stop(1,'hero/bg-end')]};
 if(g==='logo')return {type:'GRADIENT_LINEAR',gradientTransform:gT(135,w,h),gradientStops:[stop(0,'logo/gradient-start'),stop(0.5,'logo/gradient-mid'),stop(1,'logo/gradient-end')]};
 if(g==='stripes'){const a=135*Math.PI/180;const Lp=Math.abs(w*Math.sin(a))+Math.abs(h*Math.cos(a));const n=Math.ceil(Lp/10);const st=[];for(let i=0;i<n;i++){const p0=i*10/Lp,p1=Math.min(1,(i*10+5)/Lp),p2=Math.min(1,(i*10+5.001)/Lp);st.push(stop(p0,'on-gradient/soft'),stop(p1,'on-gradient/soft'),stop(p2,'misc/transparent'));if(i<n-1){const p3=Math.min(1,(i*10+9.999)/Lp);st.push(stop(p3,'misc/transparent'))}}return {type:'GRADIENT_LINEAR',gradientTransform:gT(135,w,h),gradientStops:st}}
 throw new Error('grad '+g)}
function paints(list,w,h){return (list||[]).map(p=>typeof p==='string'?solid(p):grad(p,w,h))}
const DIM={};['space/2xs','space/xs','space/sm','space/md','space/lg','space/xl','space/2xl'].forEach(n=>{if(V[n])DIM['s'+Object.values(V[n].valuesByMode)[0]]=V[n]});
['radius/sm','radius/md','radius/lg','radius/xl','radius/full'].forEach(n=>{if(V[n])DIM['r'+Object.values(V[n].valuesByMode)[0]]=V[n]});
function bindNum(node,field,val,kind){node[field]=val;const v=DIM[kind+val];if(v){try{node.setBoundVariable(field,v)}catch(e){}}}
const PA={N:'MIN',C:'CENTER',X:'MAX',S:'SPACE_BETWEEN'},CA={N:'MIN',M:'MIN',C:'CENTER',X:'MAX',B:'BASELINE'},SZ={F:'FIXED',H:'HUG',L:'FILL'};
function applyFrame(n,o){
 n.fills=paints(o.f,o.w,o.h);
 if(o.r!==undefined){if(Array.isArray(o.r)){const [tl,tr,br,bl]=o.r;bindNum(n,'topLeftRadius',tl,'r');bindNum(n,'topRightRadius',tr,'r');bindNum(n,'bottomRightRadius',br,'r');bindNum(n,'bottomLeftRadius',bl,'r')}else{const r=o.r>=Math.min(o.w,o.h)/2-0.5&&o.r>16?999:o.r;for(const f of ['topLeftRadius','topRightRadius','bottomRightRadius','bottomLeftRadius'])bindNum(n,f,r,'r')}}
 if(o.st){n.strokes=[solid(o.st.c)];n.strokeAlign=o.st.a==='O'?'OUTSIDE':'INSIDE';if(Array.isArray(o.st.w)){const [t,r,b,l]=o.st.w;n.strokeTopWeight=t;n.strokeRightWeight=r;n.strokeBottomWeight=b;n.strokeLeftWeight=l}else n.strokeWeight=o.st.w}
 if(o.op)n.opacity=o.op;
 n.clipsContent=!!o.clip;
}
async function applyFx(n,o){if(o.fx&&ES[o.fx])await n.setEffectStyleIdAsync(ES[o.fx].id)}
function setLayout(n,o){n.layoutMode=o.L==='H'?'HORIZONTAL':'VERTICAL';const p=o.pad||[0,0,0,0];bindNum(n,'paddingTop',p[0],'s');bindNum(n,'paddingRight',p[1],'s');bindNum(n,'paddingBottom',p[2],'s');bindNum(n,'paddingLeft',p[3],'s');
 if(o.pa==='S')n.primaryAxisAlignItems='SPACE_BETWEEN';else{n.primaryAxisAlignItems=PA[o.pa||'N'];bindNum(n,'itemSpacing',Math.max(0,o.gap||0),'s')}
 n.counterAxisAlignItems=(o.ca==='B'&&n.layoutMode!=='HORIZONTAL')?'MIN':CA[o.ca||'N'];
 if(o.wrap&&n.layoutMode==='HORIZONTAL'){n.layoutWrap='WRAP';n.counterAxisSpacing=o.rgap||0}
 if(o.minH)n.minHeight=o.minH;
 if(o.minW)n.minWidth=o.minW;
}
function size(n,o,parent){
 const pal=parent&&parent.type!=='PAGE'&&parent.layoutMode&&parent.layoutMode!=='NONE';
 if(o.abs&&pal){n.layoutPositioning='ABSOLUTE';n.x=o.abs[0];n.y=o.abs[1]}
 const sx=o.sx||'F',sy=o.sy||'F';
 if(sx==='F'||sy==='F'){try{n.resize(Math.max(0.01,sx==='F'?o.w:n.width),Math.max(0.01,sy==='F'?o.h:n.height))}catch(e){}}
 if(n.type==='TEXT'){n.textAutoResize=(sx==='H')?'WIDTH_AND_HEIGHT':'HEIGHT';if(o.tr){n.textTruncation='ENDING';n.maxLines=1}}
 if(pal&&!o.abs){n.layoutSizingHorizontal=SZ[sx];n.layoutSizingVertical=SZ[sy]}
 else if(n.layoutMode&&n.layoutMode!=='NONE'){if(sx==='H')n.layoutSizingHorizontal='HUG';if(sy==='H')n.layoutSizingVertical='HUG'}
}
async function setRuns(t,runs){
 const s=runs.map(r=>r[0]).join('');t.characters=s.length?s:' ';
 let i=0;for(const [txt,st,c] of runs){const j=i+txt.length;if(j>i){await t.setRangeTextStyleIdAsync(i,j,TS[st]?TS[st].id:TS['Body/Default'].id);t.setRangeFills(i,j,paints([c],t.width||100,t.height||20))}i=j}
}
async function mkText(o){const t=figma.createText();t.name=o.n||'text';await t.setTextStyleIdAsync(TS[o.tx[0][1]]?TS[o.tx[0][1]].id:TS['Body/Default'].id);await setRuns(t,o.tx);t.textAlignHorizontal={L:'LEFT',C:'CENTER',R:'RIGHT'}[o.ta||'L'];if(o.tr){t.textTruncation='ENDING';t.maxLines=1}return t}
function recolor(inst,c){inst.findAll(x=>x.type==='VECTOR'||x.type==='BOOLEAN_OPERATION').forEach(v=>{if(v.strokes&&v.strokes.length)v.strokes=[solid(c)];if(Array.isArray(v.fills)&&v.fills.length)v.fills=[solid(c)]})}
function mkIcon(o){const comp=ICON[o.ic];if(!comp)throw new Error('icon '+o.ic);const i=comp.createInstance();i.name='ic:'+o.ic;if(o.c)recolor(i,o.c);if(o.rot)i.rotation=-o.rot;return i}
async function mkGraphic(o,G){let c=GREG[o.g];if(!c){const gd=G[o.g];if(!gd)throw new Error('graphic data '+o.g);const node=figma.createNodeFromSvg(gd.svg);node.name='Graphic/'+gd.nm;
  if(gd.logo){node.findAll(x=>x.type==='VECTOR'||x.type==='ELLIPSE'||x.type==='BOOLEAN_OPERATION').forEach(v=>{v.fills=[grad({g:'logo'},v.width,v.height)]})}
  c=figma.createComponentFromNode(node);c.name='Graphic/'+gd.nm;c.setSharedPluginData(NS,'gk',o.g);stage('Graphics').appendChild(c);GREG[o.g]=c}
 const i=c.createInstance();i.name='gr:'+o.g;return i}
function arcEllipse(d,inner,start,end,color){const e=figma.createEllipse();e.resize(d,d);e.arcData={startingAngle:start,endingAngle:end,innerRadius:inner};e.fills=[solid(color)];return e}
function mkRing(o){const f=figma.createAutoLayout('VERTICAL');f.name='Ring';f.fills=[];f.primaryAxisAlignItems='CENTER';f.counterAxisAlignItems='CENTER';f.resize(46,46);f.primaryAxisSizingMode='FIXED';f.counterAxisSizingMode='FIXED';
 const tr=arcEllipse(44,36/44,0,2*Math.PI,o.c1);tr.name='Track';f.appendChild(tr);tr.layoutPositioning='ABSOLUTE';tr.x=1;tr.y=1;
 const st=-Math.PI/2,en=st+2*Math.PI*Math.min(o.p,0.9999);const ar=arcEllipse(44,36/44,st,en,o.c2);ar.name='Progress';f.appendChild(ar);ar.layoutPositioning='ABSOLUTE';ar.x=1;ar.y=1;
 for(const a of [st,en]){const cdot=figma.createEllipse();cdot.resize(4,4);cdot.fills=[solid(o.c2)];cdot.name='Cap';f.appendChild(cdot);cdot.layoutPositioning='ABSOLUTE';cdot.x=23+20*Math.cos(a)-2;cdot.y=23+20*Math.sin(a)-2}
 return f}
function mkSpin(o){const f=figma.createAutoLayout('VERTICAL');f.name='Spinner';f.fills=[];f.resize(o.w,o.h);f.primaryAxisSizingMode='FIXED';f.counterAxisSizingMode='FIXED';const inr=(o.w-2*o.bw)/o.w;
 const a=arcEllipse(o.w,inr,0,2*Math.PI,o.c2);a.name='Track';f.appendChild(a);a.layoutPositioning='ABSOLUTE';a.x=0;a.y=0;
 const b=arcEllipse(o.w,inr,-Math.PI*0.75,-Math.PI*0.25,o.c1);b.name='Arc';f.appendChild(b);b.layoutPositioning='ABSOLUTE';b.x=0;b.y=0;return f}
async function mkSwitch(o){const f=figma.createAutoLayout('HORIZONTAL');f.name='Switch';f.resize(o.w,o.h);f.primaryAxisSizingMode='FIXED';f.counterAxisSizingMode='FIXED';f.paddingLeft=f.paddingRight=f.paddingTop=f.paddingBottom=3;f.counterAxisAlignItems='CENTER';f.primaryAxisAlignItems=o.on?'MAX':'MIN';
 f.fills=paints(o.f&&o.f.length?o.f:[o.on?'brand/default':'border/default'],o.w,o.h);for(const k of ['topLeftRadius','topRightRadius','bottomRightRadius','bottomLeftRadius'])f[k]=o.h/2;
 const k=figma.createEllipse();k.name='Knob';k.resize(o.h-6,o.h-6);k.fills=[solid('switch/knob')];f.appendChild(k);await k.setEffectStyleIdAsync(ES['Shadow/Knob'].id);return f}
function mkCheck(o){const f=figma.createAutoLayout('VERTICAL');f.name='Checkbox';f.resize(o.w,o.h);f.primaryAxisSizingMode='FIXED';f.counterAxisSizingMode='FIXED';f.primaryAxisAlignItems='CENTER';f.counterAxisAlignItems='CENTER';f.fills=paints(o.f&&o.f.length?o.f:['bg/brand-soft'],o.w,o.h);const r=o.r||9;for(const k of ['topLeftRadius','topRightRadius','bottomRightRadius','bottomLeftRadius'])f[k]=r;
 if(o.on){const i=mkIcon({ic:'check-bold',c:'brand/on'});i.resize(16,16);f.appendChild(i)}return f}
async function applyOv(inst,ov){
 if(!ov)return;
 if(ov.tx){const ts=inst.findAll(n=>{if(n.type!=='TEXT')return false;let p=n.parent;while(p&&p!==inst){if(p.type==='INSTANCE'&&p.name.startsWith('gr:'))return false;p=p.parent}return true});for(let i=0;i<ov.tx.length&&i<ts.length;i++){const v=ov.tx[i];if(v==null)continue;await setRuns(ts[i],v)}}
 if(ov.sw){const ss=inst.findAll(n=>n.type==='INSTANCE'&&(n.name.startsWith('ic:')||n.name.startsWith('gr:')));for(let i=0;i<ov.sw.length&&i<ss.length;i++){const v=ov.sw[i];if(v==null)continue;if(v[0]==='i'){ss[i].swapComponent(ICON[v[1]]);if(v[2])recolor(ss[i],v[2])}else{const g=GREG[v[1]];if(g)ss[i].swapComponent(g)}}}
}
async function build(o,parent,G){
 let n;if(!o.t)o.t='f';
 if(o.cm&&o.cm.f&&REG[o.cm.k]){o={t:'inst',k:o.cm.k,sx:o.sx,sy:o.sy,w:o.w,h:o.h,abs:o.abs,grow:o.grow,ov:o.ov}}
 if(o.t==='inst'){const c=REG[o.k];if(!c)throw new Error('no comp '+o.k);n=c.createInstance();parent.appendChild(n);size(n,o,parent);await applyOv(n,o.ov);return n}
 if(o.t==='x'){n=await mkText(o)}
 else if(o.t==='i'){n=mkIcon(o)}
 else if(o.t==='g'){n=await mkGraphic(o,G)}
 else if(o.t==='ring'){n=mkRing(o)}
 else if(o.t==='spin'){n=mkSpin(o)}
 else if(o.t==='sw'){n=await mkSwitch(o)}
 else if(o.t==='cb'){n=mkCheck(o)}
 else if(o.t==='sp'){n=figma.createFrame();n.name='Spacer';n.fills=[];parent.appendChild(n);const vert=parent.layoutMode==='VERTICAL';n.resize(vert?1:o.w,vert?o.h:1);if(vert){n.layoutSizingHorizontal='FILL';n.layoutSizingVertical='FIXED'}else{n.layoutSizingVertical='FILL';n.layoutSizingHorizontal='FIXED'}if(o.grow)n.layoutGrow=1;return n}
 else {n=figma.createFrame();n.name=o.n||'frame';setLayout(n,o);applyFrame(n,o);await applyFx(n,o)}
 parent.appendChild(n);
 if(o.t==='f'){n.resize(Math.max(1,o.w||10),Math.max(1,o.h||10))}
 size(n,o,parent);
 if(o.t==='ring'){const lbl=await mkText({n:'Label',tx:o.tx,ta:'C'});n.appendChild(lbl);lbl.textAutoResize='WIDTH_AND_HEIGHT'}
 if(o.ch)for(const c of o.ch)await build(c,n,G);
 if(o.t==='f'||o.t==='ring'){if(o.sx==='H')n.layoutSizingHorizontal='HUG';if(o.sy==='H')n.layoutSizingVertical='HUG'}
 if(o.cm&&o.cm.f){
   const idx=parent.children.indexOf(n);
   const comp=figma.createComponentFromNode(n);comp.name=o.cm.b;comp.setSharedPluginData(NS,'ck',o.cm.k);comp.setSharedPluginData(NS,'cb',o.cm.b);comp.setSharedPluginData(NS,'cv',o.cm.v||'default');
   const inst=comp.createInstance();parent.insertChild(idx,inst);size(inst,o,parent);
   const st=stage('Stage/'+o.cm.b);st.appendChild(comp);try{comp.layoutSizingHorizontal=(o.sx==='H')?'HUG':'FIXED';comp.layoutSizingVertical=(o.sy==='H')?'HUG':'FIXED'}catch(e){}
   REG[o.cm.k]=comp;return inst}
 return n}
async function RUNSCREEN(D){
 const page=pages.Screens;await page.loadAsync();
 const G=D.G||{};
 const holder=figma.createFrame();holder.name='_tmp';holder.layoutMode='VERTICAL';holder.fills=[];page.appendChild(holder);
 for(const k in G){if(!GREG[k]){const gi=await mkGraphic({g:k},G);gi.remove()}}
 const scr=await build(D.root,holder,G);
 page.appendChild(scr);holder.remove();
 scr.x=D.x||0;scr.y=D.y||0;
 return scr}
