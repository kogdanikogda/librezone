S='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" width="%d" height="%d">%s</svg>'
CL='<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2M9 2.5h6"/>'
WA='<path d="M12 3.5 2.8 19.5h18.4L12 3.5Z"/><path d="M12 10v4.5M12 17.3v.1"/>'
def ic(p,s=28): return S%(s,s,p)
D={'t':('Время вышло','Вы не отправили средства за отведённые 10 минут. Обмен отменён.',CL,'err',['Понятно'],[]),
   'c':('Вы уверены, что хотите отменить обмен?','Если вы уже перевели деньги, отменять обмен не нужно.',WA,'warn',['Да, отменить'],['Нет'])}
def btns(p,o):
    return ''.join('<button class="b p">%s</button>'%x for x in p)+''.join('<button class="b o">%s</button>'%x for x in o)
def A(k):
    t,d,i,c,p,o=D[k]
    return '<div class="m mA"><span class="ico %s">%s</span><h3>%s</h3><p>%s</p><div class="bs">%s</div></div>'%(c,ic(i,30),t,d,btns(p,o))
def B(k):
    t,d,i,c,p,o=D[k]
    return '<div class="m mB"><div class="hd %s"><span class="ico2">%s</span></div><div class="bd"><h3>%s</h3><p>%s</p><div class="bs">%s</div></div></div>'%(c,ic(i,26),t,d,btns(p,o))
def C(k):
    t,d,i,c,p,o=D[k]
    return '<div class="m mC"><div class="top"><span class="ico3 %s">%s</span><h3>%s</h3></div><p>%s</p><div class="bs r">%s</div></div>'%(c,ic(i,22),t,d,btns(p,o))
V=[('A. Иконка в круге','Центрированная композиция: крупная иконка в цветном круге по смыслу (красный — отмена, янтарный — предупреждение), заголовок, текст, кнопки.',A),
   ('B. Цветная шапка','Верхняя часть окна с мягким цветным фоном и иконкой, ниже — текст и кнопки. Окно выглядит как «карточка события».',B),
   ('C. Компактный заголовок','Иконка в плитке рядом с заголовком, текст слева, кнопки в ряд. Самый сдержанный и экономит высоту.',C)]
out=''
for n,d,f in V:
    cell=''
    for th in ('','dk'):
        cell+='<div class="th %s"><small>%s</small><div class="sc"><div class="dim"></div>%s</div></div>'%(th,'Тёмная' if th else 'Светлая',f('t'))
    for th in ('','dk'):
        cell+='<div class="th %s"><small>%s</small><div class="sc"><div class="dim"></div>%s</div></div>'%(th,'Тёмная' if th else 'Светлая',f('c'))
    out+='<div class="v"><h2>%s</h2><p class="d">%s</p><div class="row">%s</div></div>'%(n,d,cell)
html='''<title>Окна и диалоги — варианты</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<style>
:root{--bg:#F6F4FC;--fg:#1B1730;--mut:#5C5878}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0D0B18;--fg:#F5F3FF;--mut:#B6B0D6;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0D0B18;--fg:#F5F3FF;--mut:#B6B0D6;color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/20px Manrope,system-ui,sans-serif;padding-block:24px;padding-inline:16px}
.w{max-width:1100px;margin:0 auto}h1{font-size:22px;line-height:28px;margin:0 0 6px;text-wrap:balance}
.lead{color:var(--mut);margin:0 0 28px;max-width:70ch}
.v{margin-bottom:36px}.v h2{font-size:16px;margin:0 0 2px}.d{margin:0 0 12px;color:var(--mut);max-width:70ch;font-size:13px;line-height:18px}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}
.th{border-radius:18px;padding:12px;min-width:0;--sf:#fff;--t:#1B1730;--t2:#5C5878;--ln:#E5E1F3;--br:#6535F5;--on:#fff;--tr:#D92D20;--trb:#FDECEA;--am:#B45F06;--amb:#FFF0D6;--pg:#F6F4FC;--dimc:rgba(14,10,30,.45);--fld:#F1EDFB;background:var(--pg)}
.th.dk{--sf:#171329;--t:#F5F3FF;--t2:#B6B0D6;--ln:#2B2549;--br:#B49CFF;--on:#0D0B18;--tr:#FF6B5E;--trb:#2E1618;--am:#F2B552;--amb:#2B2211;--pg:#0D0B18;--dimc:rgba(0,0,0,.6);--fld:#1F1A38}
.th small{display:block;font-size:11px;color:var(--t2);margin-bottom:8px;letter-spacing:.04em;text-transform:uppercase}
.sc{position:relative;border-radius:14px;padding:22px 12px;background:var(--pg);overflow:hidden;display:flex;align-items:center;min-height:250px}
.dim{position:absolute;inset:0;background:var(--dimc)}
.m{position:relative;width:100%;background:var(--sf);border-radius:22px;color:var(--t);box-shadow:0 12px 32px rgba(79,43,255,.2);overflow:hidden;box-sizing:border-box}
.m h3{margin:0;font-size:20px;line-height:26px;font-weight:700;letter-spacing:-.015em;text-wrap:balance}
.m p{margin:0;font-size:14px;line-height:21px;color:var(--t2)}
.bs{display:flex;flex-direction:column;gap:8px;margin-top:4px}.bs.r{flex-direction:row}.bs.r .b{flex:1}
.b{height:48px;border-radius:14px;border:0;font:700 15px Manrope,sans-serif;padding:0 14px}
.b.p{background:var(--br);color:var(--on)}.b.o{background:var(--fld);color:var(--t)}
.err{--c:var(--tr);--cb:var(--trb)}.warn{--c:var(--am);--cb:var(--amb)}
.mA{padding:24px 18px 18px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px}
.mA .ico{width:64px;height:64px;border-radius:50%;display:grid;place-items:center;color:var(--c);background:var(--cb);box-shadow:0 0 0 8px color-mix(in srgb,var(--cb) 45%,transparent)}
.mA .bs{align-self:stretch}.A h3{margin-top:4px}
.mB .hd{height:92px;background:var(--cb);display:grid;place-items:center;color:var(--c);position:relative}
.mB .hd::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 120%,color-mix(in srgb,var(--c) 22%,transparent),transparent 65%)}
.mB .ico2{position:relative;width:52px;height:52px;border-radius:16px;background:var(--sf);display:grid;place-items:center;box-shadow:0 6px 16px color-mix(in srgb,var(--c) 28%,transparent)}
.mB .bd{padding:16px 18px 18px;display:flex;flex-direction:column;gap:10px}
.mC{padding:18px;display:flex;flex-direction:column;gap:10px}
.mC .top{display:flex;align-items:center;gap:12px}.mC .ico3{width:40px;height:40px;border-radius:12px;flex:none;display:grid;place-items:center;color:var(--c);background:var(--cb)}
.C h3{font-size:18px;line-height:24px}
</style>
<div class="w"><h1>Окна и диалоги — три варианта оформления</h1>
<p class="lead">Сейчас окна — это белая карточка с заголовком и кнопками, без визуального акцента. Ниже три способа сделать их выразительнее; показаны «Время вышло» и подтверждение отмены в обеих темах. Выбранный стиль применю ко всем окнам: выход из аккаунта, отмена, время вышло, «Не совершайте перевод».</p>
'''+out+'</div>'
open('libre-zone-modals.html','w').write(html)
