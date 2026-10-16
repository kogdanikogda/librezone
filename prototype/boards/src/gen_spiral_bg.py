import math,sys,json
sys.path.insert(0,'variants')
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/'
def f(v): return f'{v:.2f}'
def dspiral(T,k,w0,w1,n=420,cx=50,cy=50):
    pts=[]
    for i in range(n):
        t=-T+2*T*i/(n-1); s=abs(t); sg=1 if t>=0 else -1
        pts.append((cx+sg*k*s*math.cos(s),cy+sg*k*s*math.sin(s)))
    L=[];R=[]
    for i,(x,y) in enumerate(pts):
        x0,y0=pts[max(i-1,0)];x1,y1=pts[min(i+1,len(pts)-1)]
        dx,dy=x1-x0,y1-y0;d=math.hypot(dx,dy) or 1;nx,ny=-dy/d,dx/d
        w=(w0+(w1-w0)*abs(2*i/(n-1)-1))/2
        L.append((x+nx*w,y+ny*w));R.append((x-nx*w,y-ny*w))
    P=L+R[::-1]
    path='M'+' L'.join(f'{f(x)} {f(y)}' for x,y in P)+'Z'
    caps=''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f((w0+(w1-w0)*c)/2)}"/>' for (x,y),c in ((pts[0],1),(pts[-1],1)))
    return f'<path d="{path}"/>'+caps
# толстая (знак) 1.6 оборота, поворот -45 внутри symbol
thick=dspiral(1.6*2*math.pi,42/(1.6*2*math.pi),6.5,6.5)
# тонкая линия 3.2 оборота
thin=dspiral(3.6*2*math.pi,47/(3.6*2*math.pi),1.4,1.4,n=700)
# средняя 2.4 оборота, переменная толщина
mid=dspiral(2.6*2*math.pi,46/(2.6*2*math.pi),2.2,5.5,n=600)
syms=''.join(f'<symbol id="s-{k}" viewBox="0 0 100 100" overflow="visible"><g transform="rotate(-45 50 50)" style="fill:currentColor">{v}</g></symbol>' for k,v in (('thick',thick),('thin',thin),('mid',mid)))
json.dump(syms,open(S+'spiral_bg_syms.json','w'))
print(len(syms)//1024,'KB')
