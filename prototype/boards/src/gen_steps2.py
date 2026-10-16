import json
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/'
mi=json.load(open(S+'ic2/node_modules/@iconify-json/mingcute/icons.json'))['icons']
CK='<svg viewBox="0 0 24 24" fill="currentColor">'+mi['check-fill']['body']+'</svg>'
L=['Создан','Платёж','AML','Выплата','Готово']
def cur_(c):
    o=''
    for i,l in enumerate(L):
        n=i+1;dn=n<c;nw=n==c
        a='off' if i==0 else ('on' if n<=c else '')
        b='off' if i==len(L)-1 else ('on' if n<c else '')
        o+=f'<div class="a-s"><div class="a-t"><i class="a-l {a}"></i><b class="a-b {"dn" if dn else "nw" if nw else ""}">{CK if dn else n}</b><i class="a-l {b}"></i></div><span class="{"nw" if nw else ""}">{l}</span></div>'
    return f'<div class="a-st">{o}</div>'
def ring(c):
    import math
    r=15;C=2*math.pi*r;off=C*(1-c/5)
    nxt=L[c] if c<5 else ''
    return f'<div class="b-r"><svg viewBox="0 0 40 40" width="48" height="48"><circle cx="20" cy="20" r="{r}" class="b-tr"/><circle cx="20" cy="20" r="{r}" class="b-pr" stroke-dasharray="{C:.1f}" stroke-dashoffset="{off:.1f}" transform="rotate(-90 20 20)"/></svg><b class="b-n">{c}/5</b><div><strong>{L[c-1]}</strong><small>{"Дальше: "+nxt if nxt else "Обмен завершён"}</small></div></div>'
def seg(c):
    s=''.join(f'<i class="c-g {"dn" if (i+1<c or c==5) else "nw" if i+1==c else ""}"></i>' for i in range(5))
    return f'<div class="c-w"><div class="c-gs">{s}</div><div class="c-t"><strong>{L[c-1]}</strong><small>Шаг {c} из 5</small></div></div>'
def tl(c):
    o=''
    for i,l in enumerate(L):
        n=i+1;st='dn' if (n<c or c==5) else 'nw' if n==c else ''
        o+=f'<div class="d-r {st}"><span class="d-i">{CK if (n<c or c==5) else ("<i class=pls></i>" if n==c else "")}</span><span class="d-l">{l}</span>{"<em>сейчас</em>" if n==c and c<5 else ""}</div>'
    return f'<div class="d-tl">{o}</div>'
V=[('A. Сейчас: точки с номерами','Пять точек в строке. Все этапы одинакового веса, подписи мелкие.',cur_),
 ('B. Кольцо и текущий шаг','Как в мастере создания обмена: кольцо с прогрессом, название текущего этапа и что дальше. Один акцент вместо пяти.',ring),
 ('C. Сегментная полоса','Пять тонких сегментов и одна строка: название этапа и «Шаг 3 из 5». Самый компактный.',seg),
 ('D. Вертикальный список','Все этапы списком: пройденные с галочкой, текущий выделен пульсирующей точкой, будущие приглушены. Самый понятный, но выше.',tl)]
out=''
for n,d,f in V:
    cells=''
    for th in ('','dk'):
        for c in (3,5):
            cells+=f'<div class="th {th}"><small>{"Тёмная" if th else "Светлая"} · {"этап 3" if c==3 else "завершён"}</small><div class="cd"><div class="oh"><b>MT4RAAHOS</b><span class="tg">{"В работе" if c==3 else "Завершён"}</span></div><div class="sm"><b>1 206,06 USDT → 100 000 ₽</b><span>USDT (TRX) · 1 USDT = 82,91 ₽</span></div>{f(c)}</div></div>'
    out+=f'<div class="v"><h2>{n}</h2><p class="d">{d}</p><div class="row">{cells}</div></div>'
html='''<title>Этапы заявки — варианты</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<style>
:root{--bg:#F6F4FC;--fg:#1B1730;--mut:#5C5878}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0D0B18;--fg:#F5F3FF;--mut:#B6B0D6;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0D0B18;--fg:#F5F3FF;--mut:#B6B0D6;color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/20px Manrope,system-ui,sans-serif;padding-block:24px;padding-inline:16px}
.w{max-width:1100px;margin:0 auto}h1{font-size:22px;line-height:28px;margin:0 0 6px}.lead{color:var(--mut);margin:0 0 28px;max-width:70ch}
.v{margin-bottom:32px}.v h2{font-size:16px;margin:0 0 2px}.d{margin:0 0 12px;color:var(--mut);max-width:70ch;font-size:13px;line-height:18px}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:12px}
.th{border-radius:18px;padding:12px;min-width:0;--sf:#fff;--t:#1B1730;--t2:#5C5878;--t3:#8E89A8;--ln:#E5E1F3;--br:#6535F5;--on:#fff;--soft:#EEE8FF;--ok:#0B7A5F;--okb:#DCF3EB;--pg:#F6F4FC;background:var(--pg)}
.th.dk{--sf:#171329;--t:#F5F3FF;--t2:#B6B0D6;--t3:#7F79A3;--ln:#2B2549;--br:#B49CFF;--on:#0D0B18;--soft:#241D47;--ok:#45D3A2;--okb:#0F2A23;--pg:#0D0B18}
.th>small{display:block;font-size:11px;color:var(--t2);margin-bottom:8px;letter-spacing:.04em;text-transform:uppercase}
.cd{background:var(--sf);border-radius:20px;padding:14px;color:var(--t);display:flex;flex-direction:column;gap:12px}
.oh{display:flex;justify-content:space-between;align-items:center}.oh b{font-size:13px;letter-spacing:.02em}.tg{font-size:12px;font-weight:600;padding:3px 10px;border-radius:99px;background:var(--soft);color:var(--br)}
.sm{background:var(--soft);border-radius:14px;padding:10px 14px;display:flex;flex-direction:column}.sm b{color:var(--br);font-size:16px;line-height:22px;font-weight:800}.sm span{font-size:12px;color:var(--t2)}
/* A */
.a-st{display:flex}.a-s{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;min-width:0}
.a-t{display:flex;align-items:center;width:100%}.a-l{flex:1;height:2px;background:var(--ln)}.a-l.on{background:var(--br)}.a-l.off{background:transparent}
.a-b{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-size:12px;font-weight:700;background:var(--soft);color:var(--t2);flex:none}
.a-b.dn{background:var(--br);color:var(--on)}.a-b.nw{background:var(--br);color:var(--on);box-shadow:0 0 0 4px color-mix(in srgb,var(--br) 22%,transparent)}.a-b svg{width:12px;height:12px}
.a-s span{font-size:12px;line-height:15px;color:var(--t3)}.a-s span.nw{color:var(--t);font-weight:600}
/* B */
.b-r{display:flex;align-items:center;gap:12px;position:relative}.b-r svg{flex:none}.b-tr{fill:none;stroke:var(--soft);stroke-width:4}.b-pr{fill:none;stroke:var(--br);stroke-width:4;stroke-linecap:round}
.b-n{position:absolute;left:0;width:48px;text-align:center;font-size:13px}.b-r strong{display:block;font-size:17px;line-height:22px}.b-r small{color:var(--t2);font-size:13px}
/* C */
.c-w{display:flex;flex-direction:column;gap:10px}.c-gs{display:flex;gap:4px}.c-g{flex:1;height:6px;border-radius:3px;background:var(--soft)}.c-g.dn{background:var(--br)}.c-g.nw{background:linear-gradient(90deg,var(--br) 55%,var(--soft) 55%)}
.c-t{display:flex;justify-content:space-between;align-items:baseline}.c-t strong{font-size:15px}.c-t small{color:var(--t2);font-size:12px}
/* D */
.d-tl{display:flex;flex-direction:column}.d-r{display:flex;align-items:center;gap:12px;padding:8px 0;position:relative;color:var(--t3)}
.d-r:not(:last-child)::after{content:"";position:absolute;left:11px;top:32px;bottom:-8px;width:2px;background:var(--ln)}.d-r.dn:not(:last-child)::after{background:var(--br)}
.d-i{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;border:2px solid var(--ln);box-sizing:border-box;flex:none;background:var(--sf);position:relative;z-index:1}
.d-r.dn{color:var(--t2)}.d-r.dn .d-i{background:var(--br);border-color:var(--br);color:var(--on)}.d-i svg{width:12px;height:12px}
.d-r.nw{color:var(--t);font-weight:700}.d-r.nw .d-i{border-color:var(--br)}.pls{width:10px;height:10px;border-radius:50%;background:var(--br);box-shadow:0 0 0 4px color-mix(in srgb,var(--br) 25%,transparent)}
.d-r em{margin-left:auto;font-style:normal;font-size:11px;font-weight:600;color:var(--br);background:var(--soft);padding:2px 8px;border-radius:99px}.d-l{font-size:14px}
</style>
<div class="w"><h1>Этапы заявки — варианты блока</h1>
<p class="lead">Блок из пяти точек в деталях обмена: все этапы одного веса, текущий считывается не сразу. Ниже четыре способа показать прогресс; каждый — в светлой и тёмной теме, на этапе «3 из 5» и после завершения.</p>
'''+out+'</div>'
open(S+'libre-zone-steps2.html','w').write(html)
