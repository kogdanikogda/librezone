import math, random
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/'
def f(v): return f'{v:.2f}'
def taper(pts, w0, w1, rnd=None):
    """pts: list of (x,y). width from w0 (start) to w1 (end). returns polygon path"""
    n=len(pts); L=[];R=[]
    for i,(x,y) in enumerate(pts):
        x0,y0=pts[max(i-1,0)]; x1,y1=pts[min(i+1,n-1)]
        dx,dy=x1-x0,y1-y0; d=math.hypot(dx,dy) or 1
        nx,ny=-dy/d,dx/d
        t=i/(n-1); w=(w0+(w1-w0)*t)/2
        if rnd: w*=1+rnd[i]
        L.append((x+nx*w,y+ny*w)); R.append((x-nx*w,y-ny*w))
    P=L+R[::-1]
    d='M'+' L'.join(f'{f(x)} {f(y)}' for x,y in P)+'Z'
    # round caps
    caps=''
    for (x,y),w in ((pts[0],w0),(pts[-1],w1)):
        caps+=f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(w/2)}"/>'
    return f'<path d="{d}"/>'+caps
def spiral(cx,cy,r0,r1,turns,th0=0,n=140,dirn=1):
    pts=[]
    for i in range(n):
        t=i/(n-1); r=r0+(r1-r0)*t; a=th0+dirn*turns*2*math.pi*t
        pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    return pts
def logspiral(cx,cy,r0,r1,turns,th0=0,n=160,dirn=1):
    pts=[]
    for i in range(n):
        t=i/(n-1); r=r0*(r1/r0)**t; a=th0+dirn*turns*2*math.pi*t
        pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    return pts
M={}
# A: спираль, толщина растёт к краю
M['A']=taper(spiral(50,50,4,40,2.6,-1.2),3,9)
# B: водоворот из трёх рукавов
M['B']=''.join(taper(logspiral(50,50,3,43,0.95,k*2*math.pi/3,dirn=1),2.5,11) for k in range(3))
# C: хаос — спираль с шумом и осколками
random.seed(7)
pts=spiral(50,50,3,38,2.9,0.4,n=170)
nz=[(random.random()-.5)*0.55 for _ in pts]
pj=[(x+(random.random()-.5)*3.2,y+(random.random()-.5)*3.2) for x,y in pts]
# сгладим шум скользящим средним
def smooth(p,k=4):
    o=[]
    for i in range(len(p)):
        a=max(0,i-k);b=min(len(p),i+k+1);xs=[q[0] for q in p[a:b]];ys=[q[1] for q in p[a:b]]
        o.append((sum(xs)/len(xs),sum(ys)/len(ys)))
    return o
pj=smooth(pj,5); nz=[sum(nz[max(0,i-4):i+5])/len(nz[max(0,i-4):i+5]) for i in range(len(nz))]
C=taper(pj,2.2,10,nz)
sat=''
for (x,y,r) in [(86,22,3.4),(92,40,2),(14,84,3.6),(24,92,1.8),(80,88,2.6),(8,30,2.2)]:
    sat+=f'<circle cx="{x}" cy="{y}" r="{r}"/>'
M['C']=C+sat
# D: кольца-арки со сдвигом
D=''
for i,(r,w) in enumerate([(41,6.5),(32,6),(23,5.5),(14.5,5),(7,4.5)]):
    a0=i*58; ext=290-i*18
    x0=50+r*math.cos(math.radians(a0));y0=50+r*math.sin(math.radians(a0))
    x1=50+r*math.cos(math.radians(a0+ext));y1=50+r*math.sin(math.radians(a0+ext))
    D+=f'<path d="M{f(x0)} {f(y0)} A{r} {r} 0 {1 if ext>180 else 0} 1 {f(x1)} {f(y1)}" fill="none" style="stroke:var(--mk)" stroke-width="{w}" stroke-linecap="round"/>'
M['D']=D
# E: семена (филлотаксис)
E=''
ga=math.pi*(3-math.sqrt(5))
for i in range(1,110):
    r=4.1*math.sqrt(i); a=i*ga
    x=50+r*math.cos(a);y=50+r*math.sin(a)
    if math.hypot(x-50,y-50)>44: continue
    E+=f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(0.9+r*0.075)}"/>'
M['E']=E
# F: обмен — два встречных вихря
M['F']=taper(logspiral(50,50,3,42,1.05,0.2),2.5,12)+taper(logspiral(50,50,3,42,1.05,0.2+math.pi),2.5,12)
M['F2']=None
# G: двойная спираль (S-образная, как буква Z/S в центре)
pts=[]
T=1.6*2*math.pi
for i in range(260):
    t=-T+2*T*i/259; r=2.6*t/ (2*math.pi) * 2 ; 
    k=42/T
    s=abs(t); sg=1 if t>=0 else -1
    x=50+sg*k*s*math.cos(s); y=50+sg*k*s*math.sin(s)
    pts.append((x,y))
M['G']=taper(pts,6.5,6.5)
names={
'A':('Спираль','Одна закручивающаяся линия, которая утолщается к краю. Самый спокойный и узнаваемый вариант.'),
'B':('Водоворот','Три рукава, как лопасти. Динамика и движение денег по кругу, читается как «воронка обмена».'),
'C':('Хаос','Спираль с неровной линией и разлетающимися каплями. Самый живой и «ручной» вариант, ближе всего к вашему описанию.'),
'D':('Кольца','Пять дуг, каждая сдвинута относительно предыдущей. Строгая геометрия с эффектом вращения.'),
'E':('Семена','Расположение точек как в подсолнухе: порядок, который выглядит как случайность. Намёк на блокчейн и узлы сети.'),
'F':('Обмен','Два вихря, закрученных навстречу друг другу, как две валюты в обмене. Самый смысловой вариант.'),
'G':('Двойная спираль','Одна линия входит в центр и выходит наружу, в середине получается буква S или Z. Плотный силуэт без мелких деталей.'),
}
syms=''.join(f'<symbol id="m-{k}" viewBox="0 0 100 100"><g style="fill:var(--mk)">{M[k]}</g></symbol>' for k in 'ABCDEFG')
import json
json.dump({'syms':syms,'names':names},open(S+'logo_swirl.json','w'),ensure_ascii=False)
print(len(syms)//1024,'KB')
