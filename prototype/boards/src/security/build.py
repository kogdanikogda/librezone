import base64,json
IC=json.load(open('/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ic_all.json'))
def ic(k,s=20,cls='ic'):return f'<svg class="{cls}" width="{s}" height="{s}" viewBox="0 0 24 24" aria-hidden="true">{IC[k]}</svg>'
A=base64.b64encode(open('/home/claude/sec/shield.jpg','rb').read()).decode()
B=base64.b64encode(open('/home/claude/sec/neon.jpg','rb').read()).decode()
ITEMS=[('card','Не разрешаем использовать чужие карты','Сверяем данные в личном кабинете и чеках, просим вас сверить получателя фиата.','При создании заявки'),
('bank','Автоматически проверяем подлинность перевода','Для отправки доступны только те банки, которые минимизируют возможность подделки перевода.','При переводе'),
('closec','Блокируем нарушителей','Пользователи, нарушившие правила, больше не смогут совершать обмен.','Если правила нарушены')]
NB=' '
def T(s):  # nbsp after short words
    import re
    return re.sub(r'(^|[ (])([вВсСкКуУоОиИаАяЯ]|не|на|по|за|от|до|из|Не) ',lambda m:m.group(1)+m.group(2)+NB,s)
TITLE=f'Почему обмен в{NB}Libre.zone <em>безопасен</em>?'
def ctx_top():
    return f'''<div class="sec"><h3>Для любых задач</h3><div class="tiles"><div class="tile"><span class="ti">{ic('coins',18)}</span><b>Войти в{NB}крипто&shy;инвестиции</b><small>Операции с{NB}криптой без сложных регистраций</small></div><div class="tile"><span class="ti">{ic('card',18)}</span><b>Небольшие суммы для подписок</b><small>Купите крипту для оплаты зарубежных сервисов</small></div></div></div>'''
def ctx_bot():
    return f'''<div class="sec"><h3>Почему Libre.zone?</h3><div class="why"><span class="wi">{ic('chart',20)}</span><b>Курс фиксируется при создании обмена</b></div></div>'''
def vA():
    it=''.join(f'<div class="aI"><span class="tile40">{ic(k)}</span><div><b>{T(h)}</b><p>{T(p)}</p></div></div>' for k,h,p,_ in ITEMS)
    return f'<section class="blk vA"><span class="eyebrow">{ic("shield",14)}Безопасность</span><h2>{TITLE}</h2><div class="aL">{it}</div></section>'
def vB():
    it=''.join(f'<div class="bI"><span class="btile">{ic(k)}</span><div><b>{T(h)}</b><p>{T(p)}</p></div></div>' for k,h,p,_ in ITEMS)
    return f'<section class="blk vB"><div class="bHead"><span class="bShield">{ic("shield",30)}</span><h2>{TITLE}</h2></div><div class="bL">{it}</div></section>'
def vC():
    it=''.join(f'<li>{ic("checkc",20)}<div><b>{T(h)}</b><p>{T(p)}</p></div></li>' for k,h,p,_ in ITEMS)
    return f'<section class="blk vC"><div class="cArt"><img src="data:image/jpeg;base64,{A}" alt="Щит с галочкой на фоне банковской карты"></div><h2>{TITLE}</h2><ul class="cL">{it}</ul></section>'
def vD():
    it=''.join(f'<div class="dS"><span class="dtile">{ic(k)}</span><b>{T(h)}</b><p>{T(p)}</p></div>' for k,h,p,_ in ITEMS)
    dots=''.join(f'<i{" class=on" if i==0 else ""}></i>' for i in range(len(ITEMS)))
    return f'<section class="blk vD"><div class="dBan"><img src="data:image/jpeg;base64,{B}" alt="Светящийся стеклянный щит"><h2>{TITLE}</h2></div><div class="dCar">{it}</div><div class="dDots" aria-hidden="true">{dots}</div></section>'
def vE():
    it=''.join(f'<li><span class="eDot">{ic(k,18)}</span><div><span class="eWhen">{w}</span><b>{T(h)}</b><p>{T(p)}</p></div></li>' for k,h,p,w in ITEMS)
    return f'<section class="blk vE"><h2>{TITLE}</h2><p class="eLead">Три проверки на{NB}пути каждого обмена</p><ol class="eL">{it}<li class="eEnd"><span class="eDot ok">{ic("checkc",18)}</span><div><b>Обмен защищён</b></div></li></ol></section>'
V=[('A','Мягкая панель','Ближе всего к вашему примеру: сиреневая подложка, заголовок с акцентным словом, три белые карточки с иконками. Спокойно и аккуратно, но на светлой странице выделяется слабее остальных вариантов.',vA),
('B','Тёмная плита','Тот же градиент и точечный паттерн, что у калькулятора, крупный щит в шапке, пункты разделены линиями. Самый контрастный блок ниже первого экрана — сразу ловит взгляд при прокрутке. Без растровой графики, одинаково хорошо работает в обеих темах.',vB),
('C','3D-щит','Сгенерированная в Figma иллюстрация: стеклянный щит, карта и замок. Тёплый «продуктовый» тон, пункты — компактным списком с галочками. Для тёмной темы нужна вторая картинка на тёмном фоне; здесь показан светлый вариант на плашке.',vC),
('D','Неоновый баннер · карусель','Тёмная карточка: светящийся щит с орбитой, заголовок поверх картинки, три факта — в карусели под баннером (листаются пальцем, следующая карточка выглядывает справа). Блок стал примерно вдвое ниже списка и одинаково смотрится в обеих темах.',vD),
('E','Цепочка проверок','Пункты выстроены как путь обмена: создание заявки → перевод → нарушение правил, в конце — зелёный итог «Обмен защищён». Объясняет, когда срабатывает каждая проверка, но порядок здесь условный.',vE)]
css=open('/home/claude/sec/style.css').read()
body=''
for code,name,desc,f in V:
    phones=''.join(f'<figure class="pf"><figcaption>{lab}</figcaption><div class="ph{dk}"><div class="scr">{ctx_top()}{f()}{ctx_bot()}</div></div></figure>' for lab,dk in [('Светлая тема',''),('Тёмная тема',' dk')])
    body+=f'<article class="v" id="v{code}"><header><span class="code">{code}</span><div><h2>{name}</h2><p>{desc}</p></div></header><div class="phones">{phones}</div></article>'
html=f'''<title>Блок безопасности Libre.zone</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap">
<style>{css}</style>
<main class="w">
<h1>Блок «Почему обмен безопасен» — пять вариантов</h1>
<p class="lead">Блок стоит на Главной сразу после «Для любых задач» и перед каруселью «Почему Libre.zone?». Тексты — из вашего примера. Каждый вариант показан в контексте соседних секций, в светлой и тёмной теме. Иллюстрации в вариантах C и D сгенерированы в Figma и лежат на странице Cover файла.</p>
<nav class="toc">{''.join(f'<a href="#v{c}"><b>{c}</b> {n}</a>' for c,n,_,_ in V)}</nav>
{body}
<aside class="rec"><b>Рекомендация:</b> B «Тёмная плита» — сильнее всего выделяется при прокрутке, продолжает язык калькулятора и не требует отдельной графики для тёмной темы. Если хочется больше «продуктовой» теплоты — C с иллюстрацией (сделаю вторую картинку для тёмной темы).</aside>
</main>
<script>document.querySelectorAll('.vD').forEach(v=>{{const c=v.querySelector('.dCar'),d=[...v.querySelectorAll('.dDots i')];c.addEventListener('scroll',()=>{{const w=c.firstElementChild.offsetWidth+10;const k=Math.min(d.length-1,Math.round(c.scrollLeft/w));d.forEach((e,i)=>e.classList.toggle('on',i===k))}},{{passive:true}})}})</script>'''
open('/home/claude/sec/security-variants.html','w').write(html)
print(len(html))
