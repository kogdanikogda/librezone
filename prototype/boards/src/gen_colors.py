#!/usr/bin/env python3
# Доска «Сервисные цвета Libre.zone»: 4 варианта системы статусов в палитре Индиго, светлая и тёмная тема.
OUT = '/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/libre-zone-service-colors.html'

BASE = {
    'light': dict(page='#F5F5FA', surface='#FFFFFF', field='#F1EEFB', text='#1B1730', text2='#5C5878', brand='#4B30E0', grad='linear-gradient(150deg,#1E1470,#3B25C4 55%,#6A45FF)'),
    'dark': dict(page='#0B0A16', surface='#171329', field='#1F1A38', text='#F5F3FF', text2='#B6B0D6', brand='#9C86FF', grad='linear-gradient(150deg,#140D52,#2B1C99 55%,#5236E0)'),
}
CUR = {'light': dict(ok=('#007030', '#D3F5E0'), warn=('#9A4300', '#FFEBCC'), err=('#C4121F', '#FFECEB'), info=('#4B30E0', '#ECE9FF'), neu=('#5C5878', '#EFEDF6')),
       'dark': dict(ok=('#4CC47A', '#10281B'), warn=('#FFB84D', '#2B2110'), err=('#FF8582', '#2A1517'), info=('#9C86FF', '#1E1946'), neu=('#B6B0D6', '#221E38'))}
TUNED = {'light': dict(ok=('#0B7A5F', '#DCF3EB'), warn=('#8F5200', '#FFF0D6'), err=('#C01F59', '#FDE7EF'), info=('#4B30E0', '#ECE9FF'), neu=('#5C5878', '#EFEDF6')),
         'dark': dict(ok=('#45D3A2', '#0F2A23'), warn=('#F2B552', '#2B2211'), err=('#FF7EA8', '#2E1522'), info=('#9C86FF', '#1E1946'), neu=('#B6B0D6', '#221E38'))}
MAP_OLD = dict(created='ok', pay='warn', check='warn', crypto='warn', done='ok', error='err', cancelled='err')
MAP_NEW = dict(created='neu', pay='info', check='info', crypto='info', done='ok', error='err', cancelled='neu')
LBL = [('created', 'Создан', 'checkc'), ('pay', 'Ожидание платежа', 'clock'), ('check', 'Проверка чека', 'clock'), ('crypto', 'Ожидание криптовалюты', 'clock'), ('done', 'Завершён', 'checkc'), ('error', 'Ошибка', 'closec'), ('cancelled', 'Отменён', 'closec')]

VARS = [
    ('A', 'Как сейчас', 'Стандартные зелёный, оранжевый, красный', CUR, MAP_OLD, 'fill',
     'Цвета по умолчанию из Ant Design. Сами по себе нормальные, но рядом с холодным индиго оранжевый и чистый зелёный выглядят чужими. Любой ожидающий статус оранжевый, поэтому список обменов выглядит тревожным.'),
    ('B', 'В тон индиго', 'Те же роли, подобранные оттенки', TUNED, MAP_OLD, 'fill',
     'Зелёный сдвинут к изумрудному, красный — к малиновому, оранжевый — к янтарному. Насыщенность и светлота выровнены под индиго, поэтому цвета смотрятся одной семьёй. Логика статусов прежняя.'),
    ('C', 'Процесс = бренд', 'Оттенки B + новая логика', TUNED, MAP_NEW, 'fill',
     'Обычные этапы (ожидание, проверка) окрашены в цвет бренда: это нормальный ход обмена, а не предупреждение. Янтарный остаётся только там, где нужно действие: таймер истекает, нужно подтвердить получение. Создан и Отменён — нейтральные. На экране меньше цвета, а тревожный цвет снова что-то значит.'),
    ('D', 'Приглушённые', 'Логика C, цвет только в точке', TUNED, MAP_NEW, 'dot',
     'Метки статусов нейтральные, цвет — только в точке и иконке. Самый спокойный и «дорогой» вид. Минус: статусы различаются слабее, при беглом просмотре списка хуже видно ошибки.'),
]

IC = {
    'checkc': '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'closec': '<circle cx="12" cy="12" r="9"/><path d="m9 9 6 6M15 9l-6 6"/>',
    'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    'warn': '<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
}


def ic(n, s=14):
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[n]}</svg>'


def lum(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)


def panel(key, pal, mp, style, mode):
    B = BASE[mode]; P = pal[mode]
    vars_ = ';'.join(f'--{k}:{v}' for k, v in B.items()) + ';' + ';'.join(f'--{k}:{v[0]};--{k}-bg:{v[1]}' for k, v in P.items())

    def tag(st, label, icn):
        r = mp[st]
        if style == 'dot':
            return f'<span class="tag dot" style="--c:var(--{r})"><i></i>{label}</span>'
        return f'<span class="tag" style="color:var(--{r});background:var(--{r}-bg)">{ic(icn)}{label}</span>'
    tags = ''.join(tag(*l) for l in LBL)

    def card(oid, st, label, icn, a, b):
        return f'<div class="oc"><div class="r"><b>{oid}</b>{tag(st, label, icn)}</div><div class="l"><span>{a}</span>{ic("arrow", 13)}<span>{b}</span></div></div>'
    cards = card('QMO9QSF1P', 'pay', 'Ожидание платежа', 'clock', '5 000 ₽', '60,30 USDT') + card('MT4RAAHOS', 'done', 'Завершён', 'checkc', '1 206 USDT', '100 000 ₽') + card('XK2F9QLPD', 'error', 'Ошибка', 'closec', '10 000 ₽', '120,60 USDT')
    warn_c = 'warn'

    def alert(kind, icn, title, text):
        if style == 'dot':
            return f'<div class="al soft"><span class="ai" style="color:var(--{kind});background:var(--{kind}-bg)">{ic(icn, 16)}</span><div><b>{title}</b><span>{text}</span></div></div>'
        return f'<div class="al" style="background:var(--{kind}-bg)"><span class="ai2" style="color:var(--{kind})">{ic(icn, 18)}</span><div><b style="color:var(--{kind})">{title}</b><span>{text}</span></div></div>'
    alerts = (alert('info', 'info', 'Нужна веб-версия банка', 'Подтвердите перевод в браузере.') +
              alert('ok', 'checkc', 'Средства получены', 'Отправляем USDT на ваш адрес.') +
              alert(warn_c, 'warn', 'Осталось 2 минуты', 'Успейте отправить перевод.') +
              alert('err', 'closec', 'Имя не совпадает', 'Не переводите, напишите в поддержку.'))
    timer_norm_c = 'brand'
    timers = (f'<div class="tm"><span>{ic("clock", 16)} Осталось на оплату</span><b style="color:var(--text)">09:45</b><i style="--w:96%;--c:var(--{timer_norm_c})"></i></div>'
              f'<div class="tm"><span>{ic("clock", 16)} Осталось на оплату</span><b style="color:var(--{warn_c})">01:52</b><i style="--w:18%;--c:var(--{warn_c})"></i></div>')
    field = f'<div class="fl"><small>Адрес кошелька в сети TRX</small><div class="inp" style="background:var(--err-bg)">0xe000000000000000080000</div><em style="color:var(--err)">Неверный адрес</em></div>'
    sw = ''.join(f'<span class="sw" title="{k}: {P[k][0]} / {P[k][1]} · контраст {cr(P[k][0], P[k][1]):.1f}" style="background:{P[k][1]};color:{P[k][0]}">{n}<small>{cr(P[k][0], P[k][1]):.1f}</small></span>' for k, n in (('ok', 'Успех'), ('warn', 'Внимание'), ('err', 'Ошибка'), ('info', 'Процесс'), ('neu', 'Нейтр.')))
    return f'''<div class="pv" style="{vars_}">
  <div class="mlabel">{'Светлая' if mode == 'light' else 'Тёмная'}</div>
  <div class="sws">{sw}</div>
  <div class="tags">{tags}</div>
  <div class="cards">{cards}</div>
  <div class="tms">{timers}</div>
  <div class="als">{alerts}</div>
  {field}
</div>'''


cards_html = ''
for k, t, st, pal, mp, style, d in VARS:
    rec = '<span class="rec">Рекомендую</span>' if k == 'C' else ('<span class="cur">в прототипе сейчас</span>' if k == 'A' else '')
    cards_html += f'''<article class="vcard" id="v{k}">
  <header><span class="key">{k}</span><div><h3>{t}</h3><p class="sub">{st}</p></div>{rec}</header>
  <p class="desc">{d}</p>
  <div class="pair">{panel(k, pal, mp, style, 'light')}{panel(k, pal, mp, style, 'dark')}</div>
</article>'''

HTML = f'''<title>Libre.zone: сервисные цвета</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap">
<style>
/* Варианты системы сервисных цветов: каждый вариант — светлая и тёмная панель с реальными компонентами. */
:root{{--bg:#F5F3FB;--card:#FFFFFF;--t:#16122B;--t2:#5F5978;--accent:#4B30E0;--soft:#ECE9FF;--fd:"Manrope","Inter",system-ui,sans-serif;--font:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0F0D1A;--card:#191628;--t:#F2F0FA;--t2:#A39DBD;--accent:#A58BFF;--soft:#241D44;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0F0D1A;--card:#191628;--t:#F2F0FA;--t2:#A39DBD;--accent:#A58BFF;--soft:#241D44;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--t);font-family:var(--font);font-size:15px;line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 72px}}
.wrap{{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:32px}}
.intro{{display:flex;flex-direction:column;gap:10px;max-width:760px}}
.eyebrow{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}}
h1{{font-family:var(--fd);font-size:clamp(28px,4vw,40px);line-height:1.1;margin:0;font-weight:800;text-wrap:balance}}
.intro p{{margin:0;color:var(--t2);max-width:70ch}}
.rules{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}
.rules div{{background:var(--card);border-radius:16px;padding:14px 16px;font-size:13.5px;color:var(--t2)}}
.rules b{{display:block;color:var(--t);font-size:14px;margin-bottom:2px}}
.vcard{{background:var(--card);border-radius:22px;padding:20px;display:flex;flex-direction:column;gap:14px;box-shadow:0 1px 2px rgba(30,20,70,.05),0 10px 28px -16px rgba(30,20,70,.18)}}
.vcard header{{display:flex;align-items:flex-start;gap:12px}}
.key{{flex:none;width:32px;height:32px;border-radius:10px;background:var(--t);color:var(--card);display:grid;place-items:center;font-family:var(--fd);font-weight:800}}
.vcard h3{{margin:0;font-family:var(--fd);font-size:19px;line-height:1.25}}
.sub{{margin:2px 0 0;font-size:13px;color:var(--t2)}}
.rec,.cur{{margin-left:auto;flex:none;font-size:12px;padding:3px 10px;border-radius:999px;font-weight:600;white-space:nowrap}}
.rec{{background:var(--accent);color:var(--card)}} .cur{{background:var(--soft);color:var(--accent)}}
.desc{{margin:0;font-size:14px;color:var(--t2);max-width:80ch}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
@media (max-width:820px){{.pair{{grid-template-columns:1fr}}}}
.pv{{background:var(--page);color:var(--text);border-radius:18px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0;font-size:13px}}
.mlabel{{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--text2);font-weight:600}}
.sws{{display:flex;flex-wrap:wrap;gap:6px}}
.sw{{display:flex;flex-direction:column;align-items:flex-start;padding:6px 10px;border-radius:10px;font-size:11.5px;font-weight:600;line-height:15px}}
.sw small{{font-weight:500;opacity:.8;font-size:10.5px}}
.tags{{display:flex;flex-wrap:wrap;gap:6px}}
.tag{{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;border-radius:999px;font-size:12px;line-height:16px;font-weight:600;white-space:nowrap}}
.tag.dot{{background:var(--field);color:var(--text)}}
.tag.dot i{{width:7px;height:7px;border-radius:50%;background:var(--c);display:block}}
.cards{{display:flex;flex-direction:column;gap:8px}}
.oc{{background:var(--surface);border-radius:14px;padding:12px;display:flex;flex-direction:column;gap:6px;box-shadow:0 1px 2px rgba(0,0,0,.04)}}
.oc .r{{display:flex;justify-content:space-between;align-items:center;gap:8px}}
.oc .r b{{font-size:12.5px;letter-spacing:.02em}}
.oc .l{{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--text)}}
.oc .l svg{{color:var(--text2)}}
.tms{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.tm{{background:var(--surface);border-radius:14px;padding:10px 12px;display:flex;flex-direction:column;gap:4px;position:relative;overflow:hidden}}
.tm span{{display:flex;align-items:center;gap:6px;color:var(--text2);font-size:11.5px}}
.tm b{{font-family:var(--fd);font-size:20px;line-height:24px;font-variant-numeric:tabular-nums}}
.tm i{{display:block;height:4px;border-radius:2px;background:var(--field);position:relative}}
.tm i::after{{content:"";position:absolute;inset:0 auto 0 0;width:var(--w);background:var(--c);border-radius:2px}}
.als{{display:flex;flex-direction:column;gap:8px}}
.al{{display:flex;gap:10px;padding:10px 12px;border-radius:12px;align-items:flex-start}}
.al.soft{{background:var(--surface)}}
.al b{{display:block;font-size:13px;line-height:18px}}
.al span{{font-size:12.5px;line-height:17px;color:var(--text2)}}
.ai{{width:30px;height:30px;border-radius:10px;display:grid;place-items:center;flex:none}}
.ai2{{flex:none;margin-top:1px}}
.fl{{display:flex;flex-direction:column;gap:4px}}
.fl small{{color:var(--text2);font-size:11.5px}}
.fl .inp{{border-radius:12px;padding:12px;font-family:ui-monospace,Menlo,monospace;font-size:12px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;color:var(--text)}}
.fl em{{font-style:normal;font-size:12px}}
.reco{{background:var(--card);border-radius:20px;padding:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}}
.reco h3{{margin:0 0 6px;font-family:var(--fd);font-size:17px}}
.reco p{{margin:0;color:var(--t2);font-size:14px}}
</style>
<div class="wrap">
  <div class="intro">
    <span class="eyebrow">Libre.zone · сервисные цвета · палитра Индиго</span>
    <h1>Сервисные цвета под индиго</h1>
    <p>Четыре варианта на реальных компонентах: метки статусов, карточки обменов, таймер, уведомления и ошибка поля. В образцах цвета указан контраст текста к фону. Для всех вариантов он не ниже 4,5 — норма WCAG AA.</p>
  </div>
  <div class="rules">
    <div><b>Успех</b>Обмен завершён, средства получены, данные сохранены.</div>
    <div><b>Процесс</b>Обмен идёт как обычно: ожидание, проверка, отправка. Ничего делать не нужно.</div>
    <div><b>Внимание</b>Нужно действие или время на исходе: таймер, подтверждение получения.</div>
    <div><b>Ошибка</b>Обмен не прошёл, данные неверны, нельзя продолжать.</div>
    <div><b>Нейтральный</b>Служебные состояния: создан, отменён, вне часов работы.</div>
  </div>
  {cards_html}
  <div class="reco">
    <div><h3>Что я бы выбрал: C</h3><p>Оттенки подобраны под индиго, а цвет сообщает, нужно ли что-то делать. Обычный обмен не выглядит тревожным, янтарный появляется только когда действительно пора действовать.</p></div>
    <div><h3>Если хочется спокойнее</h3><p>D — та же логика, но цвет только в точке. Подойдёт, если в интерфейсе мало статусов на одном экране.</p></div>
    <div><h3>Минимальная правка</h3><p>B — заменить оттенки и ничего не менять в логике.</p></div>
  </div>
</div>
'''
open(OUT, 'w').write(HTML)
# contrast report
for k, t, st, pal, *_ in VARS:
    for m in ('light', 'dark'):
        print(k, m, {r: round(cr(*pal[m][r]), 1) for r in pal[m]}, 'on surface:', {r: round(cr(pal[m][r][0], BASE[m]['surface']), 1) for r in ('ok', 'warn', 'err')})
