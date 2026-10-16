import math, json, random
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/'
def fit(parts, box=46, c=32):
    """parts: list of ('p',[(x,y)..]) or ('d',[(x,y,r)..]); scale into box centered at c"""
    xs=[];ys=[]
    for k,pts in parts:
        for q in pts:
            r=q[2] if k=='d' else 0
            xs+= [q[0]-r,q[0]+r]; ys+=[q[1]-r,q[1]+r]
    w=max(xs)-min(xs); h=max(ys)-min(ys); s=box/max(w,h)
    ox=c-(min(xs)+max(xs))/2*s; oy=c-(min(ys)+max(ys))/2*s
    out=[]
    for k,pts in parts:
        out.append((k,[tuple([q[0]*s+ox,q[1]*s+oy]+([q[2]*s] if k=='d' else [])) for q in pts]))
    return out, s
def pth(pts,op=None,extra=''):
    d='M'+' L'.join('%.1f %.1f'%(x,y) for x,y in pts)
    return '<path d="%s"%s%s/>'%(d,(' stroke-opacity="%s"'%op) if op else '',extra)
def render(parts):
    o=''
    for k,pts in parts:
        if k=='p': o+=pth(pts)
        elif k=='po': o+=pth(pts,'.5')
        elif k=='d': o+=''.join('<circle cx="%.1f" cy="%.1f" r="%.2f" fill="currentColor" stroke="none"/>'%q for q in pts)
    return o
def spiral(cx,cy,r0,r1,t0,t1,n=90,wob=0,ph=0):
    pts=[]
    for i in range(n+1):
        u=i/n; t=t0+(t1-t0)*u; r=r0+(r1-r0)*u
        r+=wob*math.sin(3.1*t+ph)*u
        pts.append((cx+r*math.cos(t),cy+r*math.sin(t)))
    return pts
V=[]
# 1 Архимед
p=[('p',spiral(0,0,2,26,0,5.2*math.pi))]; V.append(('Спираль','Одна непрерывная линия из центра наружу: спокойный водоворот, читается как «поток».',p,'1'))
# 2 Три рукава
p=[('p',spiral(0,0,3,26,k*2*math.pi/3,k*2*math.pi/3+2.0*math.pi*0.55)) for k in range(3)]; V.append(('Три рукава','Вихрь из трёх лопастей: динамичный, легко читается в маленьком размере.',p,'2'))
# 3 Хаос
random.seed(7)
pts=[];n=140
for i in range(n+1):
    u=i/n;t=u*5.6*math.pi;r=2+25*u**0.95+2.2*math.sin(2.7*t+1)*u+1.4*math.sin(6.1*t)*u
    pts.append((3*u*math.cos(1.2*t)+r*math.cos(t),3*u*math.sin(.8*t)+r*math.sin(t)*0.96))
p=[('p',pts)]+[('d',[(52+2*i,10-3*i,1.6-.4*i) for i in range(0)])]
V.append(('Хаос','Спираль с «дрожащим» радиусом и плывущим центром: живая, немного неровная, как нарисованная от руки.',p,'3'))
# 4 Z с завитками
def curl(E,d,R0=8,R1=2.2,turns=1.35):
    dx,dy=d; n=(-dy,dx)  # left normal
    C=(E[0]+n[0]*R0,E[1]+n[1]*R0)
    a0=math.atan2(E[1]-C[1],E[0]-C[0])
    # CCW tangent at E = rot90ccw(E-C)
    tx,ty=-(E[1]-C[1]),(E[0]-C[0]); s=1 if tx*dx+ty*dy>0 else -1
    pts=[]
    for i in range(61):
        u=i/60;a=a0+s*u*turns*2*math.pi;r=R0+(R1-R0)*u
        pts.append((C[0]+r*math.cos(a),C[1]+r*math.sin(a)))
    return pts
A=(18,20);B=(46,20);Cc=(18,46);Dd=(46,46)
# Z: A->B, B->Cc, Cc->Dd ; curl at A (continuing backwards out of A) and at Dd
zA=curl(A,(-1,0),R0=7.5,R1=2,turns=1.3)   # reaches from A going left, curling
zD=curl(Dd,(1,0),R0=7.5,R1=2,turns=1.3)
body=[A,B,Cc,Dd]
pts=list(reversed(zA))+body[1:]+zD
p=[('p',pts)]; V.append(('Z-завиток','Буква Z, у которой оба конца закручены в спираль: знак читается и как буква, и как вихрь.',p,'4'))
# 5 точки (phyllotaxis)
ga=math.radians(137.508);d=[]
for i in range(1,27):
    r=5.2*math.sqrt(i);t=i*ga
    d.append((r*math.cos(t),r*math.sin(t),3.3-2.2*(i/26)))
p=[('d',d)]; V.append(('Вихрь из точек','Частицы, разлетающиеся по золотому углу: хаотично, но по правилу. Ассоциация с распределённой сетью.',p,'5'))
# 6 двойная
p=[('p',spiral(0,0,3,26,0,2.7*math.pi)),('po',spiral(0,0,3,26,math.pi,math.pi+2.7*math.pi))]
V.append(('Двойная спираль','Две руки вращаются навстречу друг другу, вторая бледнее. Прозрачная метафора обмена «туда и обратно».',p,'6'))
# 7 арки
p=[]
for i,r in enumerate([5,10.5,16,21.5,27]):
    st=math.radians(i*68); en=st+math.radians(250-i*14)
    p.append(('p',[(r*math.cos(st+(en-st)*u/40),r*math.sin(st+(en-st)*u/40)) for u in range(41)]))
V.append(('Дуги','Вложенные дуги, каждая повёрнута относительно соседней: структура вихря без сплошной линии.',p,'7'))
# 8 Фибоначчи
r=[1,1,2,3,5,8,13];c=(0,0);P=None;pts=[];ang=math.pi
cx,cy=0,0
cur_c=(0,0);a=math.pi
for i,ri in enumerate(r):
    if i>0:
        # centre on line P->prev centre scaled
        pc=prev_c;k=ri/r[i-1]
        cur_c=(P[0]+(pc[0]-P[0])*k,P[1]+(pc[1]-P[1])*k)
        a=math.atan2(P[1]-cur_c[1],P[0]-cur_c[0])
    seg=[(cur_c[0]+ri*math.cos(a+u/30*math.pi/2),cur_c[1]+ri*math.sin(a+u/30*math.pi/2)) for u in range(31)]
    pts+=seg; P=seg[-1]; prev_c=cur_c
p=[('p',pts)]; V.append(('Золотая спираль','Дуги по числам Фибоначчи, строгая и математическая. Самый «структурный» из спиралей.',p,'8'))
out=[]
for name,desc,parts,k in V:
    f,_=fit(parts, box=46 if k!='5' else 50)
    out.append({'id':k,'name':name,'desc':desc,'svg':render(f),'dots':k=='5'})
json.dump(out,open(S+'logos_data.json','w'),ensure_ascii=False)
print(len(out),sum(len(o['svg']) for o in out)//1024,'KB')
