import json,sys,html
sys.path.insert(0,'/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ref3')
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ref3/'
setup=json.load(open(S+'setup.json'))
VV=setup['V'];TT=setup['T']
ICONS=json.load(open('/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ic_all.json'))
from tokens import ICON_FIG
FIG2KEY={v:k for k,v in ICON_FIG.items()}
MODE=0
def col(n):
    if isinstance(n,dict):
        g=n['g']
        if g=='brand':return 'linear-gradient(150deg,%s,%s 55%%,%s)'%(col('brand/gradient-start'),col('brand/gradient-mid'),col('brand/gradient-end'))
        if g=='hero':return 'linear-gradient(180deg,%s,%s)'%(col('hero/bg-start'),col('hero/bg-end'))
        if g=='hero-text':return 'linear-gradient(150deg,%s,%s 55%%,%s)'%(col('hero/text-start'),col('hero/text-mid'),col('hero/text-end'))
        if g=='stripes':return 'repeating-linear-gradient(135deg,rgba(255,255,255,.16) 0 5px,transparent 5px 10px)'
        return 'red'
    v=VV.get(n)
    if not v:return 'magenta'
    r,g,b,a=v[MODE];return 'rgba(%d,%d,%d,%s)'%(r*255,g*255,b*255,a)
FX={'Shadow/Card':'0 1px 2px rgba(30,20,70,.05),0 10px 28px -14px rgba(30,20,70,.16)','Shadow/Soft':'0 1px 2px rgba(30,20,70,.06),0 4px 12px -6px rgba(30,20,70,.12)','Shadow/Bell':'0 1px 4px rgba(27,23,48,.14)','Shadow/Brand':'0 12px 32px rgba(30,20,112,.26)','Shadow/Tabbar':'0 -10px 26px -20px rgba(30,20,112,.45)','Shadow/Dock':'0 -10px 24px -18px rgba(30,20,70,.35)','Shadow/Float':'0 4px 14px -4px rgba(0,0,0,.3)','Shadow/Thumb':'0 1px 3px rgba(30,20,70,.14)','Shadow/Plate':'0 14px 30px -14px rgba(10,6,40,.6)'}
PA={'N':'flex-start','C':'center','X':'flex-end','S':'space-between'}
CA={'N':'flex-start','M':'flex-start','C':'center','X':'flex-end','B':'baseline'}
REG={}
def font(st):
    fam,sty,size,lh,ls,U,u=TT[st]
    w={'Regular':400,'Medium':500,'Semi Bold':600,'SemiBold':600,'Bold':700,'ExtraBold':800}[sty]
    return "font-family:'%s';font-weight:%d;font-size:%spx;line-height:%s;letter-spacing:%spx;%s%s"%(fam,w,size,('%spx'%lh) if lh else 'normal',ls,'text-transform:uppercase;' if U else '','text-decoration:underline;' if u else '')
def sizing(o,parent):
    s=[];pl=parent.get('L') if parent else None
    sx=o.get('sx','F');sy=o.get('sy','F')
    if o.get('abs'):
        s.append('position:absolute;left:%spx;top:%spx;width:%spx;height:%spx'%(o['abs'][0],o['abs'][1],o.get('w',10),o.get('h',10)));return ';'.join(s)
    horiz=pl=='H'
    for ax,v in (('x',sx),('y',sy)):
        prim=(ax=='x')==horiz
        dim='width' if ax=='x' else 'height'
        if v=='F':s.append('%s:%spx;flex:none'%(dim,o.get('w' if ax=='x' else 'h',10)) if prim else '%s:%spx'%(dim,o.get('w' if ax=='x' else 'h',10)))
        elif v=='L':s.append('flex:1 1 0;min-%s:0'%dim if prim else 'align-self:stretch')
        else:
            if prim:s.append('flex:none')
    if o.get('minH'):s.append('min-height:%spx'%o['minH'])
    if o.get('minW'):s.append('min-width:%spx'%o['minW'])
    return ';'.join(s)
def render(o,parent=None,top=False):
    t=o.get('t','f')
    if t=='inst':
        m=REG[o['k']];x=apply_ov(m,o)
        if o.get('_a'):x['_a']=o['_a']
        else:x.pop('_a',None)
        return render(x,parent)
    st=sizing(o,parent)
    if t=='sp':
        return '<div style="flex:none;%s"></div>'%(('height:%spx;align-self:stretch'%o['h']) if 'h' in o else ('width:%spx;align-self:stretch'%o['w']))
    if t=='x':
        spans=''.join('<span style="%s;%s">%s</span>'%(font(r[1]),('color:'+col(r[2])) if not isinstance(r[2],dict) else 'background:%s;-webkit-background-clip:text;color:transparent'%col(r[2]),html.escape(r[0]).replace('\n','<br>')) for r in o['tx'])
        ta={'C':'center','R':'right'}.get(o.get('ta'),'left')
        ws='white-space:nowrap;' if o.get('sx')=='H' else ''
        tr='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;' if o.get('tr') else ''
        return '<div style="%s;text-align:%s;%s%s;%s">%s</div>'%(st,ta,ws,tr,font(o['tx'][0][1]),spans)
    if t=='i':
        k=FIG2KEY.get(o['ic'],o['ic']);svg=ICONS.get(k,'')
        return '<svg viewBox="0 0 24 24" fill="currentColor" style="%s;color:%s;%s">%s</svg>'%(st,col(o['c']),('transform:rotate(%sdeg)'%o['rot']) if o.get('rot') else '',svg)
    if t=='g':
        return '<div style="%s;background:#c8c8d8;border-radius:4px"></div>'%st
    if t=='ring':
        return '<div style="%s;border-radius:50%%;border:4px solid %s;display:grid;place-items:center;box-sizing:border-box"><span style="%s">%s</span></div>'%(st,col(o['c2']),font(o['tx'][0][1]),o['tx'][0][0])
    if t=='spin':
        return '<div style="%s;border-radius:50%%;border:2px solid %s"></div>'%(st,col(o['c1']))
    if t in('sw','cb'):
        bg=col(o['f'][0]) if o.get('f') else '#ccc'
        return '<div style="%s;border-radius:%spx;background:%s"></div>'%(st,o.get('r',14),bg)
    # frame
    css=['display:flex','box-sizing:border-box','position:relative','flex-direction:%s'%('row' if o.get('L')=='H' else 'column')]
    if o.get('pa')=='S':css.append('justify-content:space-between')
    else:css.append('justify-content:%s;gap:%spx'%(PA.get(o.get('pa','N')),o.get('gap',0)))
    css.append('align-items:%s'%CA.get(o.get('ca','N')))
    if o.get('wrap'):css.append('flex-wrap:wrap;row-gap:%spx'%o.get('rgap',0))
    if o.get('pad'):css.append('padding:%s'%' '.join('%spx'%p for p in o['pad']))
    if o.get('f'):
        bgs=[col(p) for p in o['f']]
        css.append('background:%s'%','.join(bgs))
    if 'r' in o:
        r=o['r'];css.append('border-radius:%s'%(' '.join('%spx'%x for x in r) if isinstance(r,list) else '%spx'%r))
    if o.get('st'):
        w=o['st']['w'];c=col(o['st']['c'])
        if isinstance(w,list):css.append('box-shadow:%s'%','.join(x for x in ['inset 0 %spx 0 %s'%(w[0],c) if w[0] else '','inset 0 -%spx 0 %s'%(w[2],c) if w[2] else ''] if x) or 'none')
        else:css.append('box-shadow:%s0 0 0 %spx %s'%('inset ' if o['st']['a']=='I' else '',w,c))
    if o.get('fx') and not o.get('st'):css.append('box-shadow:'+FX.get(o['fx'],'none'))
    if o.get('clip'):css.append('overflow:hidden')
    if o.get('op'):css.append('opacity:%s'%o['op'])
    inner=''.join(render(c,o) for c in o.get('ch',[]))
    da=(' data-a="%s"'%','.join(str(v) for v in o['_a'])) if o.get('_a') else ''
    return '<div title="%s"%s style="%s;%s">%s</div>'%(html.escape(o.get('n','')),da,';'.join(css),st,inner)
import copy
def collect(o):
    if o.get('cm') and o['cm'].get('f'):
        m=copy.deepcopy(o);REG[o['cm']['k']]=m
    for c in o.get('ch',[]):collect(c)
def apply_ov(m,o):
    n=copy.deepcopy(m)
    def _st(x):
        x.pop('_a',None)
        for c in x.get('ch',[]):_st(c)
    _st(n)
    for k in ('sx','sy','w','h','abs'):
        if k in o:n[k]=o[k]
        elif k=='abs':n.pop('abs',None)
    ov=o.get('ov') or {}
    tx=ov.get('tx');sw=ov.get('sw')
    texts=[];icons=[]
    def walk(x):
        if x.get('t')=='inst':
            # expand nested
            e=apply_ov(REG[x['k']],x);x.clear();x.update(e)
        if x.get('t') in('x','ring'):texts.append(x)
        if x.get('t') in('i','g'):icons.append(x)
        for c in x.get('ch',[]):walk(c)
    walk(n)
    if tx:
        for i,v in enumerate(tx):
            if v is not None and i<len(texts):texts[i]['tx']=v
    if sw:
        for i,v in enumerate(sw):
            if v is not None and i<len(icons) and v[0]=='i':icons[i]['ic']=v[1];icons[i]['c']=v[2] or icons[i].get('c')
    return n
FF=open('/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/t_v3.html').read().split('<style>')[1].split('</style>')[0]
if __name__=='__main__':
    ids=sys.argv[1:]
    import glob
    for f in sorted(glob.glob(S+'pay/*.json')):
        p=json.load(open(f));collect(p['root'])
        if ids and p['id'] not in ids:continue
        for MODE in (0,):
            h='<html><head><meta charset="utf-8"><style>'+FF+'body{margin:0;background:#888}</style></head><body><div style="width:390px">'+render(p['root'],None)+'</div></body></html>'
            open(S+'prev/%s.html'%p['id'],'w').write(h)
