import json,glob,sys,copy,collections,hashlib
sys.path.insert(0,'/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ref3')
import transform as T
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ref3/'

def build_root(d):
    L=d['L'];D=d['D'];mode=d['mode']
    app=L['ch'][0];dapp=D['ch'][0]
    o=T.conv(app,dapp,'app')
    o.pop('_rb',None)
    o['n']=d['id']+' '+d['name'];o['w']=390;o['sx']='F'
    o['f']=['bg/page']
    if mode=='vp':
        o['h']=844;o['sy']='F';o['clip']=1
    else:
        o['sy']='H';o['h']=L['h'];o['minH']=844
    # children of app: nav, content, tabzone
    for c in o['ch']:
        if c.get('n')=='nav' and c.get('abs'):
            c['abs']=[0,0];c['w']=390;c['sx']='F';c['sy']='F'
        if c.get('n','').startswith('content') or c.get('n') in('content',):
            if mode=='vp':
                c['sy']='L';c['clip']=1
            else:
                c['sy']='H'
        if c.get('n')=='tabzone' and c.get('abs'):
            c['abs']=[0,844-c['h']];c['w']=390
    # overlay layer
    if len(L['ch'])>1:
        lay=L['ch'][1];dlay=D['ch'][1]
        for i,c in enumerate(lay.get('ch',[])):
            cc=T.conv(c,dlay['ch'][i],'layer')
            cc['abs']=[0,0];cc['w']=390;cc['h']=844;cc['sx']='F';cc['sy']='F'
            o['ch'].append(cc)
    return o

def strip(n):
    n.pop('_rb',None)
    for c in n.get('ch',[]):strip(c)

def main(ids=None):
    files=sorted(glob.glob(S+'st/*.json'))
    if ids: files=[f for f in files if f.split('/')[-1][:2] in ids]
    roots=[]
    for f in files:
        d=json.load(open(f))
        r=build_root(d)
        T.assign_components(r)
        roots.append((d,r))
    # component meta: first occurrence order
    import os
    gk=S+'gknown.json'
    created=set();gcreated=set(json.load(open(gk)) if os.path.exists(gk) else [])
    mains={}  # k -> (texts, swaps)
    payloads=[]
    # variant naming dedupe
    vn=collections.defaultdict(list)
    for k,info in T.REG.items():
        vn[(info['b'],info['v'])].append(k)
    vname={}
    for (b,v),ks in vn.items():
        for i,k in enumerate(ks):vname[k]=v if len(ks)==1 else '%s %d'%(v,i+1)
    for d,r in roots:
        G={}
        def compact(n):
            cm=n.get('cm')
            if cm:
                k=cm['k']
                tx=T.dfs_texts(n,[]);sw=T.dfs_swaps(n,[])
                if k in created:
                    mt,ms=mains[k]
                    ovt=[None if a==b else a for a,b in zip(tx,mt)]
                    ovs=[None if a==b else list(a) for a,b in zip(sw,ms)]
                    o={'t':'inst','k':k}
                    for f in ('sx','sy','w','h','abs','grow','as','_a'):
                        if f in n:o[f]=n[f]
                    ov={}
                    if any(x is not None for x in ovt):ov['tx']=ovt
                    if any(x is not None for x in ovs):ov['sw']=ovs
                    # graphics needed by swaps
                    for a in sw:
                        if a[0]=='g' and a[1] not in gcreated:
                            G[a[1]]=T.GRAPHICS[a[1]];gcreated.add(a[1])
                    if ov:o['ov']=ov
                    return o
                created.add(k);mains[k]=(tx,sw)
                n=dict(n);n['cm']={'k':k,'b':cm['b'],'v':vname[k],'f':1}
            if n.get('t')=='g' and n['g'] not in gcreated:
                G[n['g']]=dict(T.GRAPHICS[n['g']]);gcreated.add(n['g'])
                if 'lzg' in G[n['g']]['svg']:G[n['g']]['logo']=1
            if 'ch' in n:
                n=dict(n);n['ch']=[compact(c) for c in n['ch']]
            n.pop('_rb',None)
            return n
        root=compact(r)
        # graphics names
        for k,g in G.items():
            g['nm']=g.get('nm','g')
        payloads.append({'id':d['id'],'name':d['name'],'root':root,'G':G})
    for p in payloads:
        s=json.dumps(p,ensure_ascii=False,separators=(',',':'))
        open(S+'pay/%s.json'%p['id'],'w').write(s)
    return payloads

if __name__=='__main__':
    import os;os.makedirs(S+'pay',exist_ok=True)
    ps=main(sys.argv[1:] or None)
    for p in ps:
        s=json.dumps(p,ensure_ascii=False,separators=(',',':'))
        print(p['id'],p['name'],len(s))
    print('components',len(T.REG),'bases',len(set(v['b'] for v in T.REG.values())))
    print('unknown colors',T.UNKNOWN.most_common(30))
    print('unknown fonts',T.UNKNOWN_FONT)
    c=collections.Counter(v['b'] for v in T.REG.values());print(c.most_common())
