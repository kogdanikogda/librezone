#!/usr/bin/env python3
# Доска «Libre.zone: визуальные варианты» — скриншоты из прототипа + логотипы SVG + промпты для Figma
import base64, io
from PIL import Image
S = '/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/'
V = S + 'v3/shots/vis/'
OUT = S + 'libre-zone-visual-variants.html'


def img(path, w=300, crop=None):
    im = Image.open(path).convert('RGB')
    if crop:
        im = im.crop(crop)
    h = int(im.height * w / im.width)
    im = im.resize((w * 2, h * 2), Image.LANCZOS) if im.width >= w * 2 else im.resize((w, h), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


def shot(path, alt, crop=None):
    return f'<img class="shot" src="{img(path, 300, crop)}" alt="{alt}" loading="lazy">'

# кадрирование: телефон 760? скриншоты #phone ~ 390x844 *1.5
probe = Image.open(V + 'pal_aurora.png'); PW, PH = probe.size
CALC = (0, int(PH * .10), PW, int(PH * .88))
HERO = (0, 0, PW, int(PH * .62))

PALS = [
    ('aurora', 'Aurora', 'Текущая', ['#4F2BFF', '#8349FF', '#D447D6'], 'Яркий трёхцветный градиент от синего-фиолетового к розовому.'),
    ('soft', 'Мягкий', 'Градиент едва заметен', ['#5A3CF2', '#7A52F4'], 'Два близких фиолетовых. Спокойнее и дороже на вид, меньше «неона».'),
    ('indigo', 'Индиго', 'Глубже и строже', ['#1E1470', '#3B25C4', '#6A45FF'], 'Тёмный индиго с подсветкой. Хорошо для финтеха: солидно, белый текст читается лучше всего.'),
    ('sky', 'Небо', 'Холоднее', ['#5B3BFF', '#4C6BFF', '#2FA8FF'], 'Фиолетовый уходит в голубой. Ассоциация с TON и Telegram — уместно для Mini App.'),
    ('orchid', 'Орхидея', 'Теплее', ['#6A2BFF', '#B23DDB', '#FF6F91'], 'Фиолетовый уходит в розово-коралловый. Самая эмоциональная, ближе к lifestyle.'),
    ('mono', 'Моно', 'Почти без градиента', ['#7454FF', '#5F3CF0'], 'Один фиолетовый с лёгким вертикальным переходом. Чище всего, ближе к вашему исходному дизайну.'),
]

HEROS = [
    ('rings', 'Кольца', 'Текущий', 'Концентрические орбиты и монета. Векторный, лёгкий.', None),
    ('mesh', 'Пятна', 'Mesh-градиент', 'Мягкие цветовые пятна брендовых оттенков. Без рисунка, только свет.',
     'Soft abstract mesh gradient, blurred blobs of violet #6535F5, magenta #D447D6 and light blue, very light lavender background, airy, minimal, smooth, no text, no objects'),
    ('glow', 'Сияние', 'Северное сияние', 'Размытые световые ленты по диагонали — отсылка к названию Aurora.',
     'Soft aurora borealis light ribbons in violet, blue and pink, heavily blurred, flowing diagonally, on a very light lavender background, airy and minimal, empty space on the left, no text'),
    ('space', 'Космос', 'Тёмный hero', 'Глубокий космос, звёзды и фиолетовая планета. Самый эффектный, hero становится тёмным в обеих темах.',
     'Deep violet outer space, soft purple and magenta nebula clouds, a glowing violet planet partially visible at the right edge, scattered tiny stars, smooth gradients, cinematic but minimal, large empty dark area on the left for text, no text, no logos'),
    ('topo', 'Рельеф', 'Линии-изолинии', 'Тонкие топографические линии. Паттерн вместо картинки, хорошо масштабируется.', None),
    ('grid', 'Сетка', 'Перспектива', 'Уходящая в перспективу сетка — «цифровое пространство», без картинок.', None),
    ('glass', 'Стекло', '3D-объекты', 'Глянцевые стеклянные сферы. В прототипе нарисованы CSS, для продакшена — 3D-картинка.',
     'Abstract 3D composition of glossy translucent glass spheres and a floating coin-like disc, violet, magenta and blue tones, soft studio lighting, subtle reflections and refraction, very light lavender background, objects on the right side, empty space on the left for text, no text, no logos'),
]

LOGOS = [
    ('ring', 'Кольцо', 'Текущий', '<circle cx="12" cy="12" r="5.6" stroke-width="2.2"/>', 'Простое кольцо — «зона». Нейтральный, легко узнаётся в фавиконе.'),
    ('lz', 'LZ', 'Монограмма', '<path d="M6.6 6.5v11h4.2" stroke-width="2.2"/><path d="M11.2 6.5h6.4l-6.4 11h6.4" stroke-width="2.2"/>', 'Буквы L и Z сцеплены. Работает как самостоятельный знак без названия.'),
    ('swap', 'Обмен', 'Две стрелки', '<path d="M6.6 12.4a5.4 5.4 0 0 1 9.3-4.3" stroke-width="2.1"/><path d="M16.4 5.2v3.3h-3.3" stroke-width="2.1"/><path d="M17.4 11.6a5.4 5.4 0 0 1-9.3 4.3" stroke-width="2.1"/><path d="M7.6 18.8v-3.3h3.3" stroke-width="2.1"/>', 'Прямо говорит «обмен». Минус: похожие знаки у многих обменников.'),
    ('hex', 'Соты', 'Открытый шестиугольник', '<path d="M15.2 7.3l2.4 1.4v6.6L12 18.6l-5.6-3.3V8.7L12 5.4" stroke-width="2.1"/><circle cx="12" cy="12" r="1.7" fill="currentColor" stroke="none"/>', 'Блок блокчейна с открытой гранью — свобода (Libre) и децентрализация.'),
    ('orbit', 'Орбита', 'Планета', '<circle cx="12" cy="12" r="3.2" fill="currentColor" stroke="none"/><ellipse cx="12" cy="12" rx="8" ry="3.1" transform="rotate(-28 12 12)" stroke-width="1.8"/>', 'Связан с фоном «Космос» и кольцами hero. Хорош для анимации.'),
    ('gate', 'Арка', 'Открытый вход', '<path d="M7.4 18.2v-6.6a4.6 4.6 0 0 1 9.2 0v6.6" stroke-width="2.2"/><circle cx="12" cy="14.6" r="1.4" fill="currentColor" stroke="none"/>', 'Открытая дверь — «свободный вход» без документов и селфи.'),
]

WHYS = [
    ('slider', 'Слайдер', 'Как в вашем дизайне', 'Одна карточка, точки снизу, листается свайпом. Компактно, но 4 из 5 пунктов скрыты.'),
    ('carousel', 'Карусель', 'Видна следующая карточка', 'Край следующей карточки подсказывает, что можно листать. Видно больше, чем в слайдере.'),
    ('list', 'Список', 'Все 5 сразу', 'Одна карточка, все пункты видны без жестов. Лучше для доверия, но длиннее.'),
    ('bento', 'Плитки', 'Главное крупно', 'Первый пункт (фиксированный курс) крупно на градиенте, остальные 4 — сеткой 2×2.'),
]


def logo_cell(k, t, st, svg, d):
    def mark(size, bg, fg, r):
        return f'<span class="lmark" style="width:{size}px;height:{size}px;border-radius:{r}px;background:{bg};color:{fg}"><svg viewBox="0 0 24 24" width="{int(size*.8)}" height="{int(size*.8)}" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">{svg}</svg></span>'
    g = 'linear-gradient(135deg,#4F2BFF,#8349FF 50%,#D447D6)'
    return f'''<article class="card" id="logo-{k}">
  <header><div><h3>{t}</h3><p class="sub">{st}</p></div></header>
  <div class="lstage">
    <div class="lrow light">{mark(28, g, '#fff', 9)}<span class="word">Libre<b>.zone</b></span></div>
    <div class="lrow dark">{mark(28, g, '#fff', 9)}<span class="word">Libre<b>.zone</b></span></div>
    <div class="lrow icons">{mark(64, g, '#fff', 18)}{mark(40, '#16122B', '#fff', 12)}{mark(40, '#FFFFFF', '#5A34E8', 12)}{mark(18, g, '#fff', 5)}</div>
  </div>
  <p class="desc">{d}</p>
</article>'''


def sw(cols):
    return '<div class="sw">' + ''.join(f'<span style="background:{c}" title="{c}"></span>' for c in cols) + f'<i style="background:linear-gradient(90deg,{",".join(cols)})"></i></div>'


pal_cards = ''.join(f'''<article class="card" id="pal-{k}">
  <header><div><h3>{t}</h3><p class="sub">{st}</p></div>{'<span class="cur">в прототипе сейчас</span>' if k == 'aurora' else ''}</header>
  {sw(cols)}
  <div class="pair">{shot(V + f'pal_{k}.png', t + ', светлая', CALC)}{shot(V + f'pald_{k}.png', t + ', тёмная', CALC)}</div>
  <p class="desc">{d}</p>
</article>''' for k, t, st, cols, d in PALS)


def prompt_block(p, k):
    if not p:
        return '<p class="note">Делается кодом или вектором, картинка не нужна.</p>'
    return f'''<div class="prompt"><div class="ph"><span>Промпт для генерации в Figma</span><button class="copy" data-copy="pr-{k}">Копировать</button></div><code id="pr-{k}">{p}</code></div>'''


hero_cards = ''.join(f'''<article class="card" id="hero-{k}">
  <header><div><h3>{t}</h3><p class="sub">{st}</p></div>{'<span class="cur">в прототипе сейчас</span>' if k == 'rings' else ''}</header>
  {shot(V + f'hero_{k}.png', t, HERO)}
  <p class="desc">{d}</p>
  {prompt_block(p, k)}
</article>''' for k, t, st, d, p in HEROS)

logo_cards = ''.join(logo_cell(*l) for l in LOGOS)

why_cards = ''.join(f'''<article class="card" id="why-{k}">
  <header><div><h3>{t}</h3><p class="sub">{st}</p></div>{'<span class="cur">по умолчанию</span>' if k == 'slider' else ''}</header>
  {shot(V + f'why_{k}.png', t)}
  <p class="desc">{d}</p>
</article>''' for k, t, st, d in WHYS)

old_calc = shot(S + 'v3/shots/eta_a_light.png', 'Было', (0, 60, Image.open(S + 'v3/shots/eta_a_light.png').width, 600))
new_calc = shot(V + 'calc_new.png', 'Стало', (0, 215, PW, 1065))

HTML = f'''<title>Libre.zone: визуальные варианты</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap">
<style>
/* Доска вариантов: секции по задачам, карточка = вариант со скриншотом из прототипа. */
:root{{--bg:#F5F3FB;--surface:#FFFFFF;--text:#16122B;--text2:#5F5978;--line:#E4DFF2;--accent:#5A34E8;--soft:#EEE9FF;--code:#F4F1FC;
 --fd:"Manrope","Inter",system-ui,sans-serif;--font:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0F0D1A;--surface:#191628;--text:#F2F0FA;--text2:#A39DBD;--line:#2C2742;--accent:#A58BFF;--soft:#241D44;--code:#211C35;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0F0D1A;--surface:#191628;--text:#F2F0FA;--text2:#A39DBD;--line:#2C2742;--accent:#A58BFF;--soft:#241D44;--code:#211C35;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:var(--font);font-size:15px;line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 72px}}
.wrap{{max-width:1200px;margin:0 auto;display:flex;flex-direction:column;gap:56px}}
.intro{{display:flex;flex-direction:column;gap:10px;max-width:740px}}
.eyebrow{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}}
h1{{font-family:var(--fd);font-size:clamp(28px,4vw,40px);line-height:1.1;margin:0;font-weight:800;text-wrap:balance}}
h2{{font-family:var(--fd);font-size:24px;line-height:1.2;margin:0;font-weight:800}}
.intro p,.sec-head p{{margin:0;color:var(--text2);max-width:68ch}}
nav.toc{{display:flex;flex-wrap:wrap;gap:8px}}
nav.toc a{{padding:6px 12px;border-radius:999px;background:var(--surface);color:var(--text);text-decoration:none;font-size:13px;box-shadow:0 1px 2px rgba(30,20,70,.06)}}
section{{display:flex;flex-direction:column;gap:20px}}
.sec-head{{display:flex;flex-direction:column;gap:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}}
.grid.wide{{grid-template-columns:repeat(auto-fill,minmax(360px,1fr))}}
.card{{background:var(--surface);border-radius:20px;padding:18px;display:flex;flex-direction:column;gap:14px;min-width:0;box-shadow:0 1px 2px rgba(30,20,70,.05),0 10px 28px -16px rgba(30,20,70,.18)}}
.card header{{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}}
.card h3{{margin:0;font-family:var(--fd);font-size:18px;line-height:1.25;font-weight:700}}
.sub{{margin:2px 0 0;font-size:13px;color:var(--text2)}}
.cur{{flex:none;font-size:11.5px;line-height:16px;padding:3px 9px;border-radius:999px;background:var(--soft);color:var(--accent);font-weight:600;white-space:nowrap}}
.desc{{margin:0;font-size:14px;color:var(--text2)}}
.shot{{display:block;width:100%;max-width:100%;height:auto;border-radius:14px;background:var(--bg)}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.sw{{display:flex;align-items:center;gap:6px}}
.sw span{{width:22px;height:22px;border-radius:7px;flex:none}}
.sw i{{flex:1;height:22px;border-radius:7px;display:block}}
.prompt{{background:var(--code);border-radius:12px;padding:10px 12px;display:flex;flex-direction:column;gap:6px}}
.ph{{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:12px;color:var(--text2);font-weight:600;letter-spacing:.02em}}
.prompt code{{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:12px;line-height:1.5;color:var(--text);user-select:all;overflow-wrap:anywhere}}
.copy{{border:0;border-radius:999px;padding:4px 10px;background:var(--surface);color:var(--accent);font-size:12px;font-weight:600;cursor:pointer}}
.copy:focus-visible,nav.toc a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.note{{margin:0;font-size:12.5px;color:var(--text2)}}
.lstage{{display:flex;flex-direction:column;gap:8px}}
.lrow{{display:flex;align-items:center;gap:10px;padding:14px;border-radius:14px}}
.lrow.light{{background:#F6F5FB;color:#1B1730}}
.lrow.dark{{background:#0D0B18;color:#F5F3FF}}
.lrow.dark .word b{{color:#B49CFF}}
.lrow.icons{{background:var(--bg);gap:14px;flex-wrap:wrap}}
.lmark{{display:grid;place-items:center;flex:none;box-shadow:0 1px 2px rgba(0,0,0,.08)}}
.word{{font-family:var(--fd);font-weight:800;font-size:21px;letter-spacing:-.02em}}
.word b{{color:#6535F5}}
.ba{{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}}
.ba figure{{margin:0;display:flex;flex-direction:column;gap:8px}}
.ba figcaption{{font-size:13px;font-weight:600;color:var(--text2)}}
.groups{{display:flex;flex-direction:column;gap:12px;margin:0;padding:0;list-style:none}}
.groups li{{display:flex;gap:12px;align-items:flex-start}}
.groups b{{flex:none;width:26px;height:26px;border-radius:8px;background:var(--soft);color:var(--accent);display:grid;place-items:center;font-family:var(--fd);font-size:13px}}
.groups span{{font-size:14px;color:var(--text2)}}
.groups strong{{color:var(--text);font-weight:600}}
.calcwrap{{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:24px;align-items:start}}
@media (max-width:760px){{.calcwrap{{grid-template-columns:1fr}}}}
@media (max-width:420px){{.grid,.grid.wide{{grid-template-columns:1fr}}}}
</style>
<div class="wrap">
  <div class="intro">
    <span class="eyebrow">Libre.zone · визуальный язык</span>
    <h1>Варианты оформления главной</h1>
    <p>Блок обмена, шесть палитр рядом с текущей, семь фонов первого блока, шесть логотипов и четыре раскладки блока «Почему Libre.zone». Всё, кроме логотипов, снято из прототипа — там каждый вариант включается в панели слева.</p>
    <nav class="toc" aria-label="Разделы"><a href="#calc">Блок обмена</a><a href="#pal">Палитры</a><a href="#hero">Фон первого блока</a><a href="#logo">Логотип</a><a href="#why">Почему Libre.zone</a></nav>
  </div>

  <section id="calc">
    <div class="sec-head"><h2>Блок обмена: группы вместо сплошного списка</h2>
      <p>Раньше восемь строк шли подряд с одинаковым шагом. Теперь три группы с разным расстоянием внутри и между ними.</p></div>
    <div class="calcwrap">
      <div class="ba"><figure>{old_calc}<figcaption>Было</figcaption></figure><figure>{new_calc}<figcaption>Стало</figcaption></figure></div>
      <ul class="groups">
        <li><b>1</b><span><strong>Пара и курс.</strong> «Отдаю», «Получаю» и курс собраны в одну подложку: это один расчёт. Курс переехал внутрь, к цифрам, которые он объясняет.</span></li>
        <li><b>2</b><span><strong>Сумма.</strong> Заголовок «Сумма в рублях», кнопки и подсказка про время ожидания идут вплотную, отступ 10 px.</span></li>
        <li><b>3</b><span><strong>Действие.</strong> Кнопка отделена от сумм большим отступом, между группами — 18 px.</span></li>
      </ul>
    </div>
  </section>

  <section id="pal">
    <div class="sec-head"><h2>Палитры рядом с Aurora</h2><p>Все сохраняют фиолетовую основу. Отличаются силой градиента и оттенком, в который он уходит. Слева светлая тема, справа тёмная.</p></div>
    <div class="grid wide">{pal_cards}</div>
  </section>

  <section id="hero">
    <div class="sec-head"><h2>Фон первого блока</h2><p>Кольца, рельеф и сетка делаются кодом. Для пятен, сияния, космоса и стекла в прототипе стоят CSS-заглушки, а в продакшене их лучше заменить картинкой. Промпты ниже можно вставить в генерацию изображений в Figma.</p></div>
    <div class="grid">{hero_cards}</div>
  </section>

  <section id="logo">
    <div class="sec-head"><h2>Логотип</h2><p>Знак на градиентной плашке с названием, на светлом и тёмном фоне, и в размерах иконки приложения, аватара Telegram-бота и фавикона.</p></div>
    <div class="grid">{logo_cards}</div>
  </section>

  <section id="why">
    <div class="sec-head"><h2>Почему Libre.zone: пять пунктов</h2><p>Пять пунктов из вашего дизайна: фиксированный курс, получение по СБП, без селфи и документов, проверка и безопасность, без скрытых комиссий. По умолчанию в прототипе слайдер, как у вас.</p></div>
    <div class="grid">{why_cards}</div>
  </section>
</div>
<script>
document.addEventListener('click',function(e){{var b=e.target.closest('.copy');if(!b)return;var el=document.getElementById(b.getAttribute('data-copy'));var t=el.textContent;
 var done=function(){{b.textContent='Скопировано';setTimeout(function(){{b.textContent='Копировать'}},1600)}};
 try{{navigator.clipboard.writeText(t).then(done,function(){{var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Выделено'}})}}catch(_){{var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r)}}}});
</script>
'''
open(OUT, 'w').write(HTML)
print('ok', round(len(HTML) / 1024), 'KB')
