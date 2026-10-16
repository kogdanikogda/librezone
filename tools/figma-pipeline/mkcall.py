import sys,json
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ref3/'
def call(pid,store=False,x=0,y=0,reset=False):
    p=json.load(open(S+'pay/%s.json'%pid));p['x']=x;p['y']=y
    import re
    RX=re.compile(r'(^|[ \u00a0(«])([вВсСкКуУоОиИаАяЯ]) ')
    def nb(runs):
        for r in runs:
            if r and isinstance(r[0],str):r[0]=RX.sub(lambda m:m.group(1)+m.group(2)+'\u00a0',RX.sub(lambda m:m.group(1)+m.group(2)+'\u00a0',r[0]))
    def cl(n):
        if n.get('tx'):nb(n['tx'])
        ov=n.get('ov')
        if ov and ov.get('tx'):
            for v in ov['tx']:
                if v:nb(v)
        for k in ('blk','inl','wr','as','_a','_nw','_nh'):
            n.pop(k,None)
        if n.get('n')=='' :n.pop('n')
        if n.get('pa')=='N':n.pop('pa')
        if n.get('ca')=='N':n.pop('ca')
        if n.get('gap')==0:n.pop('gap')
        if n.get('ta')=='L':n.pop('ta')
        if n.get('t')=='f':n.pop('t')
        for c in n.get('ch',[]):
            if c.get('t')=='x' and c.get('sx')=='L' and n.get('sx')=='H' and n.get('L')=='V':c['sx']='H'
            cl(c)
        if 'ch' in n and not n['ch']:n.pop('ch')
    cl(p['root'])
    d=json.dumps(p,ensure_ascii=False,separators=(',',':'))
    for nk,ok in {'0a1eb9e2':'382efe22','812ff4d3':'3c15bda7','d43536e9':'bb2ed366','119f10c9':'d47af980'}.items():d=d.replace('"'+nk+'"','"'+ok+'"')
    src=open(S+'compiler.js').read()
    pre=("const SRC=String.raw`"+src+"`;figma.root.setSharedPluginData('lzone','compiler',SRC);\n") if store else "const SRC=figma.root.getSharedPluginData('lzone','compiler');\n"
    rs=("{const sp=figma.root.children.find(p=>p.name==='Screens');await sp.loadAsync();sp.children.forEach(n=>n.remove());const cp=figma.root.children.find(p=>p.name==='Components');await cp.loadAsync();cp.children.filter(n=>n.name.startsWith('Stage/')).forEach(n=>n.remove());}\n") if reset else ''
    code=pre+rs+"const D="+d+";\nconst AF=Object.getPrototypeOf(async function(){}).constructor;\nconst scr=await (new AF('figma','D',SRC+'\\nreturn await RUNSCREEN(D);'))(figma,D);\nreturn {id:scr.id,name:scr.name,w:scr.width,h:scr.height};"
    return code
if __name__=='__main__':
    pid=sys.argv[1];store=len(sys.argv)>2 and sys.argv[2]=='1'
    x=float(sys.argv[3]) if len(sys.argv)>3 else 0
    reset='reset' in sys.argv
    open(S+'call.js','w').write(call(pid,store,x,0,reset))
