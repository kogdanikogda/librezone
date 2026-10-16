# usage: mkover2.py base pid [pid...]  -> call.js with clones of base + overlays
import sys,json
sys.path.insert(0,'.')
import mkcall
base=sys.argv[1];pids=sys.argv[2:]
out="""const SRC=figma.root.getSharedPluginData('lzone','compiler');
const AF=Object.getPrototypeOf(async function(){}).constructor;
const run=new AF('figma','D',SRC+'\\nreturn await RUNSCREEN(D);');
const pg=figma.root.children.find(p=>p.name==='Screens');await figma.setCurrentPageAsync(pg);
const base=pg.children.find(n=>n.name.startsWith('%s '));const res=[];
async function make(name,x,OV,G){const scr=base.clone();scr.name=name;scr.x=x;scr.y=0;
for(const c of [...scr.children])if(c.layoutPositioning==='ABSOLUTE')c.remove();
for(const o of OV){let n;if(o.t==='inst'){const tmp=await run(figma,{root:{n:'tmp',w:390,h:60,L:'V',sx:'F',sy:'H',ch:[o]},G,x:0,y:0});n=tmp.children[0];scr.appendChild(n);tmp.remove()}else{n=await run(figma,{root:o,G,x:0,y:0});scr.appendChild(n)}n.layoutPositioning='ABSOLUTE';n.x=0;n.y=0;}
res.push(scr.id);return scr}
"""%base
for pid in pids:
    code=mkcall.call(pid,False,0,0)
    d=json.loads(code.split('const D=',1)[1].split(';\nconst AF',1)[0])
    ovs=[c for c in d['root']['ch'] if c.get('abs')]
    for o in ovs:o.pop('abs',None)
    out+="await make(%s,%d,%s,%s);\n"%(json.dumps(d['root']['n'],ensure_ascii=False),(int(pid)-1)*450,json.dumps(ovs,ensure_ascii=False,separators=(',',':')),json.dumps(d['G'],ensure_ascii=False,separators=(',',':')))
out+="for(const id of res){const n=await figma.getNodeByIdAsync(id);await n.screenshot({scale:0.6})}\nreturn res;"
open('call.js','w').write(out);print(len(out))
