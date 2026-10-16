import sys,json
sys.path.insert(0,'/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ref3')
import mkcall
S=mkcall.S
ids=sys.argv[1:]
Ds=[]
for pid in ids:
    code=mkcall.call(pid,False,(int(pid)-1)*450,0)
    d=code.split('const D=',1)[1].split(';\nconst AF',1)[0]
    Ds.append(d)
out="const SRC=figma.root.getSharedPluginData('lzone','compiler');\nconst AF=Object.getPrototypeOf(async function(){}).constructor;\nconst run=new AF('figma','D',SRC+'\\nreturn await RUNSCREEN(D);');\nconst res=[];\n"
for d in Ds:
    out+="{const D="+d+";const s=await run(figma,D);res.push([s.name,Math.round(s.height)]);}\n"
out+="return res;"
open(S+'call.js','w').write(out);print(len(out))
