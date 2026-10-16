import json,re,hashlib,sys,collections
sys.path.insert(0,'/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ref3')
from tokens import PAIRS,EXTRA,TEXT,ICON_FIG
from colors import norm
UNKNOWN=collections.Counter()
UNKNOWN_FONT=collections.Counter()

def tok(a,b,ctx=''):
    na=norm(a) if a else None; nb=norm(b) if b else None
    if nb is None: nb='none'
    k=(na,nb)
    if k in PAIRS: return PAIRS[k]
    # fallback: match light only (unique)
    c=[v for (l,d),v in PAIRS.items() if l==na]
    UNKNOWN[(na,nb,ctx)]+=1
    return c[0] if c else 'misc/'+(na or 'x').replace('#','').replace('/','_')

def is_transparent(c):
    return c is None or re.match(r'rgba\(\s*0,\s*0,\s*0,\s*0\)',c) is not None

def split_layers(s):
    out=[];d=0;cur=''
    for ch in s:
        if ch=='(':d+=1
        if ch==')':d-=1
        if ch==',' and d==0: out.append(cur.strip());cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur.strip())
    return out

def grad_paint(Ls,Ds):
    """return paint spec list for background-image strings"""
    if Ls is None: return []
    if Ls.startswith('linear-gradient(150deg, rgb(30, 20, 112)'): return [{'g':'brand'}]
    if Ls.startswith('linear-gradient(rgb(236, 234, 251)'): return [{'g':'hero'}]
    if Ls.startswith('repeating-linear-gradient(135deg'): return [{'g':'stripes'}]
    UNKNOWN[('GRAD',Ls[:80],'')]+=1
    return []

def text_color(a,b,ctx):
    if a and a.startswith('G:'):
        if 'rgb(30, 20, 112)' in a: return {'g':'hero-text'}
        return {'g':'brand'}
    return tok(a,b,ctx)

def font(f):
    if f not in TEXT:
        UNKNOWN_FONT[f]+=1
        return 'Body/Default'
    return TEXT[f]

# ---------------- component rules ----------------
def first_cls(n): return (n.get('cls') or '').split()
RULES=[
 # (predicate, base, variant_fn)
 (lambda c,n: 'nav' in c, 'Header', lambda c,n:'over' if 'over' in c else 'default'),
 (lambda c,n: 'tabs' in c, 'Tab bar', None),
 (lambda c,n: 'tab' in c and n.get('tag')=='button', 'Tab item', lambda c,n:'active' if 'on' in c else 'default'),
 (lambda c,n: 'plate' in c, 'Active order', None),
 (lambda c,n: 'bell' in c, 'Bell button', None),
 (lambda c,n: 'logo' in c, 'Logo', None),
 (lambda c,n: 'btn' in c, 'Button', lambda c,n:' '.join(x for x in c if x not in('btn','ia','one'))+(' disabled' if n.get('dis') else '')),
 (lambda c,n: 'tag' in c, 'Status tag', lambda c,n:[x for x in c if x in('ok','err','info','neu','warn')][0] if any(x in c for x in ('ok','err','info','neu','warn')) else 'default'),
 (lambda c,n: 'fld' in c, 'Field', None),
 (lambda c,n: 'inp' in c, 'Input', lambda c,n:' '.join(x for x in c if x!='inp') or 'default'),
 (lambda c,n: 'sel' in c, 'Select', None),
 (lambda c,n: any(x in c for x in ('notebox','warnbox','okbox')), 'Notice', lambda c,n:[x for x in c if x.endswith('box')][0].replace('box','')),
 (lambda c,n: 'eta' in c, 'ETA note', None),
 (lambda c,n: 'stepring' in c, 'Step progress', lambda c,n:'order' if 'in' in c else 'exchange'),
 (lambda c,n: 'ocard' in c, 'Order card', None),
 (lambda c,n: 'fchip' in c, 'Filter chip', lambda c,n:'selected' if n.get('pressed')=='true' else 'default'),
 (lambda c,n: 'chip' in c and n.get('tag')=='button', 'Amount chip', lambda c,n:('selected' if n.get('pressed')=='true' else 'default')+(' slow' if 'slow' in c else '')),
 (lambda c,n: 'tile' in c, 'Task tile', None),
 (lambda c,n: 'ws' in c, 'Feature card', None),
 (lambda c,n: 'partner' in c, 'Partner card', None),
 (lambda c,n: 'dcard' in c, 'Document card', None),
 (lambda c,n: 'hours' in c, 'Hours card', None),
 (lambda c,n: 'hcell' in c, 'Hours cell', None),
 (lambda c,n: 'histi' in c, 'History item', None),
 (lambda c,n: 'rv' in c, 'Review row', None),
 (lambda c,n: 'stat' in c, 'Stat row', None),
 (lambda c,n: 'row' in c and 'ia' in c, 'List row', None),
 (lambda c,n: 'opt' in c, 'Option row', lambda c,n:'selected' if n.get('selected')=='true' else 'default'),
 (lambda c,n: 'nitem' in c, 'Notification row', lambda c,n:'unread' if 'unread' in c else 'read'),
 (lambda c,n: 'sumstrip' in c, 'Summary strip', None),
 (lambda c,n: 'sumline' in c, 'Order amount', None),
 (lambda c,n: 'timer' in c, 'Timer', lambda c,n:'urgent' if 'warn' in c else 'default'),
 (lambda c,n: 'notify' in c, 'Telegram notify', None),
 (lambda c,n: 'wait' in c, 'Waiting', None),
 (lambda c,n: 'check' in c and n.get('tag')=='label', 'Agreement', None),
 (lambda c,n: 'back' in c, 'Back link', None),
 (lambda c,n: 'foot' in c, 'Footer', None),
 (lambda c,n: 'seg2' in c, 'Segmented', None),
 (lambda c,n: 'copy-i' in c or 'mini-copy' in c, 'Copy button', lambda c,n:' '.join(c)),
 (lambda c,n: 'curpill' in c, 'Currency pill', None),
 (lambda c,n: 'swapbtn' in c, 'Swap button', None),
 (lambda c,n: 'mic' in c, 'Modal icon', lambda c,n:' '.join(x for x in c if x!='mic')),
 (lambda c,n: 'nic' in c, 'Notification icon', lambda c,n:' '.join(x for x in c if x!='nic')),
 (lambda c,n: any(x in c for x in ('ti','hi','wi2')), 'Icon tile', lambda c,n:' '.join(c)),
 (lambda c,n: 'bdot' in c, 'Bank logo', lambda c,n:'full' if 'full' in c else 'default'),
 (lambda c,n: 'tok' in c, 'Coin', None),
 (lambda c,n: 'rep' in c, 'Repeat button', None),
 (lambda c,n: 'badge' in c, 'Fee badge', None),
 (lambda c,n: 'bdg' in c or 'bdg2' in c, 'Counter', lambda c,n:' '.join(c)),
 (lambda c,n: 'link' in c and n.get('tag')=='button', 'Pill link', None),
 (lambda c,n: 'xbtn2' in c, 'Close button', None),
 (lambda c,n: 'grab' in c, 'Grabber', None),
 (lambda c,n: 'sh' in c and n.get('tag')=='div', 'Sheet header', None),
 (lambda c,n: 'modal' in c, 'Modal', lambda c,n:' '.join(x for x in c if x!='modal') or 'default'),
 (lambda c,n: 'mcode' in c or ('code' in c and n.get('tag')=='div'), 'Code input', None),
 (lambda c,n: 'refbox' in c, 'Referral info', None),
 (lambda c,n: 'dsum' in c, 'Doc summary', None),
 (lambda c,n: n.get('t')=='sw', 'Switch', lambda c,n:'on' if n.get('on') else 'off'),
 (lambda c,n: n.get('t')=='cb', 'Checkbox', lambda c,n:'checked' if n.get('on') else 'default'),
 (lambda c,n: n.get('t')=='ring', 'Ring', None),
 (lambda c,n: n.get('t')=='spin', 'Spinner', None),
]
def rule_for(n):
    c=first_cls(n)
    for pred,base,vf in RULES:
        try:
            if pred(c,n): return base,(vf(c,n) if vf else 'default')
        except Exception: pass
    return None,None

# ---------------- conversion ----------------
def aimap(ai,horizontal):
    if ai in('center',):return 'C'
    if ai in('flex-end','end'):return 'X'
    if ai=='baseline' and horizontal:return 'B'
    if ai in('flex-start','start','self-start','baseline'):return 'M'
    return 'N'
def jcmap(jc):
    return {'center':'C','flex-end':'X','end':'X','space-between':'S'}.get(jc,'N')

def has_wrap_text(n):
    if n.get('t')=='x' and n.get('wr'):return True
    return any(has_wrap_text(c) for c in n.get('ch',[]) if not c.get('abs'))

def leaf_fixed(n):
    # frame with no text descendants in-flow (icons, graphics, empty boxes)
    def hastext(x):
        if x.get('t')=='x':return True
        return any(hastext(c) for c in x.get('ch',[]) if not c.get('abs'))
    return n.get('t') in ('f',) and not hastext(n)

GRAPHICS={}
def gkey(svg):
    return hashlib.md5(svg.encode()).hexdigest()[:10]

def paints_for(L,D,ctx):
    ps=[]
    if L.get('bg') and not is_transparent(L['bg']): ps.append(tok(L['bg'],D.get('bg'),'bg:'+ctx))
    if L.get('bgi'): ps+=grad_paint(L['bgi'],D.get('bgi'))
    return ps

EFFECT_SIGS=[
 ((0,1,2,0),'Shadow/Card'),((0,1,2,0,'s'),'Shadow/Soft'),
]
def effect_for(L,D):
    sh=[s for s in L.get('sh',[]) if not (s['x']==0 and s['y']==0 and s['b']==0)]
    if not sh:return None
    key=tuple((s['x'],s['y'],s['b'],s['s']) for s in sh)
    c0=norm(sh[0]['c'])
    table={((0,1,2,0),(0,10,28,-14)):'Shadow/Card',((0,1,2,0),(0,4,12,-6)):'Shadow/Soft',((0,1,4,0),):'Shadow/Bell',((0,12,32,0),):'Shadow/Brand',
           ((0,-10,26,-20),):'Shadow/Tabbar',((0,-10,24,-18),):'Shadow/Dock',((0,4,14,-4),):'Shadow/Float',((0,1,3,0),):'Shadow/Thumb',((0,14,30,-14),):'Shadow/Plate'}
    if key in table:return table[key]
    UNKNOWN[('FX',str(key),c0)]+=1
    return None
def strokes_for(L,D,ctx):
    st=None
    sp=[(i,s) for i,s in enumerate(L.get('sh',[])) if s['x']==0 and s['y']==0 and s['b']==0 and s['s']>0]
    if sp:
        i,s=sp[0];ds=D.get('sh',[]);dc=ds[i]['c'] if i<len(ds) else None
        st={'c':tok(s['c'],dc,'ring:'+ctx),'w':s['s'],'a':'I' if s['i'] else 'O'}
    bd=L.get('bd')
    if bd and not st:
        dbd=D.get('bd') or {}
        sides=[bd.get(k,[0,None])[0] for k in 'trbl']
        k0=[k for k in 'trbl' if k in bd][0]
        st={'c':tok(bd[k0][1],dbd.get(k0,[0,None])[1],'bd:'+ctx),'w':sides if len(set(sides))>1 else sides[0],'a':'I'}
    return st

def conv(L,D,ctx,parent=None):
    t=L.get('t')
    o={}
    cls=L.get('cls') or ''
    nm=(cls.split()[0] if cls else '') or L.get('tag','')
    o['n']=nm
    b,v=rule_for(L)
    if b: o['_rb']=[b,v]
    o['w']=round(L['w'],1);o['h']=round(L['h'],1)
    if 'ax' in L: o['_a']=[L['ax'],L['ay'],round(L['w']),round(L['h'])]
    if L.get('abs'): o['abs']=[round(L['x'],1),round(L['y'],1)]
    if L.get('grow'): o['grow']=1
    if L.get('as'): o['as']=L['as']
    if L.get('op'): o['op']=L['op']
    if L.get('rot'): o['rot']=L['rot']
    if t=='x':
        o['t']='x'
        runs=[]
        for i,r in enumerate(L['runs']):
            dr=D['runs'][i] if i<len(D.get('runs',[])) else r
            txt=r['t'].replace('­','')
            if 'U' in r['f'].split('|')[5:6]: txt=txt.upper()
            runs.append([txt,font(r['f']),text_color(r['c'],dr['c'],'text:'+ctx)])
        o['tx']=runs
        o['ta']={'center':'C','right':'R','end':'R'}.get(L.get('ta'),'L')
        o['wr']=1 if L.get('wrap') else 0
        if L.get('trunc'): o['tr']=1
        if L.get('anon') or L.get('disp')=='inline': o['inl']=1
        if L.get('tw') is not None: o['_nw']=L['tw'];o['_nh']=L['th']
        return o
    if t=='i':
        o['t']='i';o['ic']=ICON_FIG.get(L['k'],L['k']);o['c']=tok(L['col'],D.get('col'),'icon:'+ctx);return o
    if t=='g':
        svg=L['svg']
        svg=re.sub(r'\s(class|aria-hidden|style)="[^"]*"','',svg)
        if 'url(#lzg)' in svg:
            svg=svg.replace('<g ','<defs><linearGradient id="lzg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="100" y2="100"><stop offset="0" stop-color="#4F2BFF"/><stop offset=".5" stop-color="#8349FF"/><stop offset="1" stop-color="#D447D6"/></linearGradient></defs><g ',1)
        k=gkey(svg)
        if k not in GRAPHICS:
            GRAPHICS[k]={'svg':svg,'nm':{'mark':'Logo mark','tok':'Coin','nb':'Network','bdot':'Bank'}.get(ctx,'Graphic')+' '+k[:4]}
        o['t']='g';o['g']=k;return o
    if t=='ring':
        da=[float(x) for x in L['da'].split()]
        o.update({'t':'ring','p':round(da[0]/da[1],3),'c1':tok(L['tc'],D['tc'],'ringtrack'),'c2':tok(L['rc'],D['rc'],'ring'),
                  'tx':[[L['lbl']['t'],font(L['lbl']['f']),tok(L['lbl']['c'],D['lbl']['c'],'ringlbl')]]})
        return o
    if t=='spin':
        o.update({'t':'spin','c1':tok(L['c1'],D['c1'],'spin1'),'c2':tok(L['c2'],D['c2'],'spin2'),'bw':L['bw']});return o
    if t in('sw','cb'):
        o['t']=t;o['on']=L.get('on',0)
        o['f']=paints_for(L,D,ctx)
        if L.get('r') is not None:o['r']=L['r']
        return o
    # frame
    o['t']='f'
    f=paints_for(L,D,nm)
    if f:o['f']=f
    if L.get('r') is not None:o['r']=L['r']
    st=strokes_for(L,D,nm)
    if st:o['st']=st
    fx=effect_for(L,D)
    if fx:o['fx']=fx
    if L.get('clipx'):o['clip']=1
    if L.get('clipy'):o['clip']=1;o['sy']='F'
    if L.get('pad'):o['pad']=L['pad']
    if L.get('minH') and L['minH']>L['h']-0.5 and L['minH']<=L['h']+0.5: o['minH']=L['minH']
    lay=L.get('L')
    chL=[c for c in L.get('ch',[])];chD=D.get('ch',[])
    kids=[]
    for i,c in enumerate(chL):
        dc=chD[i] if i<len(chD) else c
        if c.get('t')=='f' and not c.get('ch') and (c['w']<0.5 or c['h']<0.5): continue
        kids.append((c,dc))
    # grid handling
    if lay=='G':
        cols=L.get('cols',1)
        inflow=[k for k in kids if not k[0].get('abs')]
        if cols>1 and len(inflow)>cols:
            o['L']='V';o['gap']=L.get('rgap',0);o['ca']='N';o['pa']='N'
            rows=[]
            for i in range(0,len(inflow),cols):
                rows.append(inflow[i:i+cols])
            o['ch']=[]
            for r in rows:
                ro={'t':'f','n':'row','L':'H','gap':L.get('gap',0),'pa':'N','ca':'N','sx':'L','sy':'H','ch':[],'w':round(sum(c['w'] for c,dc in r)+L.get('gap',0)*(len(r)-1),1),'h':max(c['h'] for c,dc in r)}
                for c,dc in r:
                    cc=conv(c,dc,nm,ro);cc['sx']='L';cc['sy']=cc.get('sy') or ('L' if L.get('ai') in('normal','stretch') else 'H')
                    if cc['sy']=='L':cc['sy']='L'
                    ro['ch'].append(cc)
                finalize(ro,None)
                o['ch'].append(ro)
            for c,dc in kids:
                if c.get('abs'):o['ch'].append(conv(c,dc,nm,o))
            return finalize(o,L)
        elif cols>1:
            o['L']='H';o['gap']=L.get('gap',0);o['pa']='N';o['ca']=aimap(L.get('ai'),True)
            if L.get('ai') in ('normal','stretch'): o['ca']='N'
            o['ch']=[]
            # widest text-holding child fills
            ws=[(c['w'],i) for i,(c,dc) in enumerate(kids) if not c.get('abs')]
            for i,(c,dc) in enumerate(kids):
                cc=conv(c,dc,nm,o)
                o['ch'].append(cc)
            inf=[cc for cc,(c,dc) in zip(o['ch'],kids) if not c.get('abs')]
            if len(inf)==cols and len(set(round(c['w']) for c in inf))==1:
                for cc in inf: cc['sx']='L'
            else:
                mx=max(inf,key=lambda c:c['w']) if inf else None
                if mx is not None: mx['sx']='L'
            if L.get('ai') in ('normal','stretch'):
                for cc in inf:
                    if cc.get('t')=='f' and not cc.get('sy'): cc['sy']='L'
            return finalize(o,L)
        else:
            lay='V1'
    if lay in ('H','V'):
        o['L']=lay;o['gap']=L.get('gap',0) or 0
        o['pa']=jcmap(L.get('jc'));o['ca']=aimap(L.get('ai'),lay=='H')
        if L.get('wrap'):o['wrap']=1;o['rgap']=L.get('rgap',0)
    elif lay=='V1':
        o['L']='V';o['gap']=L.get('rgap',0) or 0;o['pa']=jcmap(L.get('jc'));o['ca']=aimap(L.get('ai'),False)
        if L.get('ji')=='center' or L.get('ai')=='center':o['ca']='C'
        if L.get('jc') in ('center',) or L.get('ai')=='center':o['pa']='C' if L.get('ai')=='center' else o['pa']
    else: # block
        o['L']='V';o['gap']=0;o['pa']='N';o['ca']='N';o['blk']=1
        if L.get('ta')=='center':o['ca']='C'
    o['ch']=[conv(c,dc,nm,o) for c,dc in kids]
    # margins -> inset wrappers (vertical containers)
    if o['L']=='V':
        pad=o.get('pad') or [0,0,0,0]
        innerW=L['w']-pad[1]-pad[3]
        for cc,(c,dc) in zip(o['ch'],kids):
            if c.get('abs') or cc.get('t') not in (None,'f'):continue
            ml=c['x']-pad[3]; mr=(pad[3]+innerW)-(c['x']+c['w'])
            cp=cc.get('pad')
            if (ml<-0.5 or mr<-0.5) and cp:
                cp=list(cp)
                if ml<-0.5 and cp[3]>=-ml: cp[3]=round(cp[3]+ml,1);c['x']=pad[3]
                if mr<-0.5 and cp[1]>=-mr: cp[1]=round(cp[1]+mr,1)
                cc['pad']=cp;cc['w']=innerW;c['w']=innerW
        for i,(cc,(c,dc)) in enumerate(zip(list(o['ch']),kids)):
            if c.get('abs') or cc.get('t')=='sp':continue
            ml=c['x']-pad[3]; mr=(pad[3]+innerW)-(c['x']+c['w'])
            istext=cc.get('t')=='x'
            if istext and (ml<1.5 or cc.get('inl') or o.get('ca')!='N'):continue
            if ml>1.5 and mr>-0.5 and c['w']<innerW-2 and o.get('ca')=='N':
                if (abs(ml-mr)<1.5 and ml>40) or mr<1.5:
                    wrap={'t':'f','n':'align','L':'V','ca':'X' if mr<1.5 else 'C','w':innerW,'h':c['h'],'sx':'L','sy':'H','ch':[cc]}
                    if cc.get('sx')=='L':cc['sx']='F'
                else:
                    cc['sx']='L'
                    wrap={'t':'f','n':'inset','L':'V','pad':[0,round(mr),0,round(ml)],'w':innerW,'h':c['h'],'sx':'L','sy':'H','ch':[cc]}
                finalize(wrap,None)
                o['ch'][i]=wrap
    # leading offset -> padding
    inflow0=[(cc,c) for cc,(c,dc) in zip(o['ch'],kids) if not c.get('abs')]
    if o['L'] in('V','H') and o.get('pa') in (None,'N','S') and inflow0:
        pad=list(o.get('pad') or [0,0,0,0])
        if o['L']=='V':
            lead=inflow0[0][1]['y']-pad[0]
            if (0.5<lead<40) or (lead<-0.5 and pad[0]>=-lead): pad[0]=round(pad[0]+lead,1);o['pad']=pad
        else:
            lead=inflow0[0][1]['x']-pad[3]
            if ((0.5<lead<40) or (lead<-0.5 and pad[3]>=-lead)) and o.get('pa')!='C': pad[3]=round(pad[3]+lead,1);o['pad']=pad
            last=inflow0[-1][1];trail=(L['w']-pad[1])-(last['x']+last['w'])
            if (trail<-0.5 and pad[1]>=-trail) or (o.get('pa')=='S' and 0.5<trail<40): pad[1]=round(pad[1]+trail,1);o['pad']=pad
    # ordered list markers
    if L.get('tag')=='ol':
        pad=list(o.get('pad') or [0,0,0,0]);ind=pad[3];pad[3]=0;o['pad']=pad
        for i,cc in enumerate(o['ch']):
            if cc.get('t')=='x' and cc['tx'] and re.match(r'^\d+\. ',cc['tx'][0][0]):
                m=re.match(r'^(\d+\.) ',cc['tx'][0][0]);num=m.group(1)
                rest=[list(r) for r in cc['tx']];rest[0][0]=rest[0][0][len(m.group(0)):]
                o['ch'][i]={'t':'f','n':'li','L':'H','gap':4,'w':cc['w']+ind,'h':cc['h'],'sx':'L','sy':'H','ch':[
                    {'t':'x','n':'marker','tx':[[num,cc['tx'][0][1],cc['tx'][0][2]]],'ta':'R','w':ind-4,'h':cc['h'],'sx':'F','sy':'H'},
                    dict(cc,tx=rest,sx='L',sy='H',w=cc['w'])]}
    # gap inference / spacers
    inflow=[(cc,c) for cc,(c,dc) in zip(o['ch'],kids) if not c.get('abs')]
    if o['L'] in('V','H') and o.get('pa')!='S' and len(inflow)>1 and not o.get('wrap'):
        ax='y' if o['L']=='V' else 'x'; sz='h' if o['L']=='V' else 'w'
        gaps=[round(inflow[i+1][1][ax]-(inflow[i][1][ax]+inflow[i][1][sz]),1) for i in range(len(inflow)-1)]
        g0=o['gap']
        if all(abs(g-gaps[0])<0.8 for g in gaps):
            if gaps[0]>-0.5: o['gap']=max(0,round(gaps[0]))
        else:
            # insert spacers
            base=0
            newch=[];it=iter(range(len(inflow)))
            seq=[cc for cc in o['ch']]
            infl=[cc for cc,c in inflow]
            out=[]
            for cc in seq:
                out.append(cc)
                if cc in infl:
                    i=infl.index(cc)
                    if i<len(gaps):
                        extra=round(gaps[i]-base)
                        if extra>0:
                            spn={'t':'sp','n':'spacer',('h' if o['L']=='V' else 'w'):extra}
                            if o['L']=='H' and extra>16 and gaps[i]==max(gaps):
                                lastc=inflow[-1][1];padr=(o.get('pad') or [0,0,0,0])[1]
                                if abs((lastc['x']+lastc['w'])-(L['w']-padr))<2: spn['grow']=1
                            out.append(spn)
                        elif extra<-0.5 and o['L']=='V':
                            pd=cc.get('pad')
                            if pd and pd[2]>=-extra: pd[2]=pd[2]+extra; cc['h']=cc.get('h',0)+extra
            o['ch']=out;o['gap']=base
    return finalize(o,L)

def natural(c):
    ch=[x for x in c.get('ch',[]) if not x.get('abs')]
    if not ch or c.get('t') not in (None,'f'):return None
    pad=c.get('pad') or [0,0,0,0];g=c.get('gap',0) or 0
    def sz(x,k):
        if x.get('t')=='x' and ('_n'+k) in x:return x['_n'+k]
        return x.get(k,0)
    if c.get('L')=='H':
        w=sum(sz(x,'w') for x in ch)+g*(len(ch)-1)+pad[1]+pad[3];h=max(sz(x,'h') for x in ch)+pad[0]+pad[2]
    else:
        h=sum(sz(x,'h') for x in ch)+g*(len(ch)-1)+pad[0]+pad[2];w=max(sz(x,'w') for x in ch)+pad[1]+pad[3]
    if c.get('pa')=='S':
        if c.get('L')=='H':w=0
        else:h=0
    return w,h
def finalize(o,L):
    if o.get('ch'):
        o['ch']=[c for c in o['ch'] if not c.get('abs')]+[c for c in o['ch'] if c.get('abs')]
    # sizing of children based on this container
    lay=o.get('L')
    for c in o.get('ch',[]):
        if c.get('abs'):
            c['sx']='F';c['sy']='F';continue
        if c.get('t')=='sp':continue
        horiz=(lay=='H')
        stretch=(o.get('ca')=='N')
        prim='sx' if horiz else 'sy'; cross='sy' if horiz else 'sx'
        if c.get('t')=='x':
            if c.get(prim) is None:
                c[prim]='L' if c.get('grow') else 'H'
            if c.get(cross) is None:
                pad=o.get('pad') or [0,0,0,0];iw=(o.get('w') or 0)-pad[1]-pad[3]
                c[cross]='L' if ((stretch and not horiz) or (not horiz and c.get('wr') and abs(c.get('w',0)-iw)<2.5)) else 'H'
            if c.get('wr') or c.get('tr'):
                pad=o.get('pad') or [0,0,0,0]
                inner=o.get('w',0)-pad[1]-pad[3]
                if not horiz:
                    c['sx']='L' if (abs(c.get('w',0)-inner)<1.5 or c.get('inl')) else 'F'
                elif c['sx']=='H':c['sx']='F'
            if c['sx']=='L' and c['sy']=='H':pass
            continue
        if c.get('t') in ('i','g','ring','spin','sw','cb'):
            c.setdefault('sx','F');c.setdefault('sy','F');continue
        # frame
        pad=o.get('pad') or [0,0,0,0]
        innerW=(o.get('w') or 0)-pad[1]-pad[3]; innerH=(o.get('h') or 0)-pad[0]-pad[2]
        if c.get(prim) is None:
            if c.get('grow'):c[prim]='L'
            elif leaf_fixed(c):c[prim]='F'
            elif prim=='sx' and has_wrap_text(c):c[prim]='F'
            else:c[prim]='H'
        if c.get(cross) is None:
            asf=c.get('as')
            full=(abs(c.get('w',0)-innerW)<2.5) if cross=='sx' else (abs(c.get('h',0)-innerH)<2.5)
            if (stretch and (asf in (None,'stretch','normal')) and (full or not o.get('w'))) or (full and o.get('w') and not leaf_fixed(c)):c[cross]='L'
            elif leaf_fixed(c):c[cross]='F'
            elif cross=='sx' and has_wrap_text(c):c[cross]='F'
            else:c[cross]='H'
        # overflowing children -> fixed cross size
        if c.get('L') in ('H','V') and c.get('ch'):
            pad=c.get('pad') or [0,0,0,0]
            infl=[x for x in c['ch'] if not x.get('abs') and x.get('t')!='sp']
            if c.get('h') and c['L']=='H' and infl and max(x.get('h',0) for x in infl)>c.get('h',0)-pad[0]-pad[2]+1.5 and c.get('sy')=='H': c['sy']='F'
            if c.get('w') and c['L']=='V' and infl and max(x.get('w',0) for x in infl)>c.get('w',0)-pad[1]-pad[3]+1.5 and c.get('sx')=='H': c['sx']='F'
        if horiz and c.get('sy')=='L' and not c.get('minH'): c['minH']=round(c.get('h',0),1)
        nat=natural(c)
        if nat:
            nw,nh=nat
            if c.get('sy')=='H' and c.get('h',0)>nh+1.5 and not c.get('minH'): c['minH']=round(c['h'],1)
            if c.get('sx')=='H' and c.get('w',0)>nw+1.5 and not c.get('minW'): c['minW']=round(c['w'],1)
    return o

# ---------------- signatures / components ----------------
def sig(n):
    """structure signature ignoring text content and icon/graphic identity"""
    if n.get('cm'): return 'C:'+n['cm']['k']
    t=n.get('t')
    parts=[t,n.get('n',''),n.get('sx',''),n.get('sy','')]
    if n.get('sx')=='F' or t in('i','g','ring','spin','sw','cb'): parts.append(str(round(n.get('w',0))))
    if n.get('sy')=='F' or t in('i','g','ring','spin','sw','cb'): parts.append(str(round(n.get('h',0))))
    for k in ('L','gap','pad','pa','ca','wrap','rgap','f','r','st','fx','clip','minH','op','rot','c','c1','c2','on','ta','wr','tr','abs','p'):
        if k in n:
            v=n[k]
            if k=='abs':v=[round(v[0]),round(v[1])]
            parts.append(k+'='+json.dumps(v,ensure_ascii=False))
    if t=='x' or t=='ring':
        parts.append('S='+json.dumps([[len(r[0])>0,r[1],r[2]] for r in n['tx']],ensure_ascii=False) if t=='x' and len(n['tx'])>1 else 'S='+json.dumps([n['tx'][0][1],n['tx'][0][2]],ensure_ascii=False))
    if t=='sp': parts.append(str(n.get('h',n.get('w'))))
    parts.append('['+','.join(sig(c) for c in n.get('ch',[]))+']')
    return '|'.join(parts)

REG={}   # sigkey -> {k, base, v}
COUNT=collections.Counter()
def assign_components(n):
    for c in n.get('ch',[]): assign_components(c)
    base,var=rule_for_node(n)
    if not base: return
    s=sig(n)
    h=hashlib.md5(s.encode()).hexdigest()[:8]
    if h not in REG:
        COUNT[base]+=1
        REG[h]={'k':h,'b':base,'v':var,'new':True}
    n['cm']={'k':h,'b':base,'v':REG[h]['v']}

def rule_for_node(n):
    return tuple(n['_rb']) if n.get('_rb') else (None,None)

def attach_src(o,L):
    """walk converted tree and attach source nodes for rule matching (parallel structure except grid rows/spacers)"""
    pass

def dfs_texts(n,out):
    if n.get('t') in('x','ring'): out.append(n['tx'])
    for c in n.get('ch',[]): dfs_texts(c,out)
    return out
def dfs_swaps(n,out):
    if n.get('t')=='i': out.append(('i',n['ic'],n.get('c')))
    if n.get('t')=='g': out.append(('g',n['g'],None))
    for c in n.get('ch',[]):
        dfs_swaps(c,out)
    return out
