#!/usr/bin/env python3
# Таблица статусов Libre.zone: строки — статусы, столбцы — варианты цвета текста/фона. Светлая и тёмная тема.
OUT = '/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/libre-zone-statuses.html'

ST = [('Создан', 'neu', 'Заявка создана, ждём реквизиты'), ('Ожидание платежа', 'info', 'Ждём ваш перевод: рубли или крипту'), ('Проверка чека', 'info', 'Покупка: проверяем оплату'),
      ('Ожидание криптовалюты', 'info', 'Покупка: отправляем крипту'), ('Проверка AML', 'info', 'Продажа: проверяем поступление'),
      ('Ожидание фиата', 'info', 'Продажа: отправляем рубли'), ('Завершён', 'ok', 'Обмен успешно закрыт'), ('Отменён', 'neu', 'Отменён клиентом или по таймеру'),
      ('Ошибка', 'err', 'Обмен не прошёл'), ('Время на исходе', 'warn', 'Таймер меньше 2 минут'), ('Открыто', 'ok', 'Часы работы: принимаем заявки'), ('Закрыто', 'neu', 'Часы работы: вне расписания')]

# (bg, fg, dot) per role
V = [
 ('soft', 'Мягкая', 'В прототипе сейчас', {
   'light': dict(info=('#ECE9FF', '#3B25C4', '#5B3FF0'), ok=('#E1F5EE', '#0A6B53', '#14A57F'), err=('#FCE8EF', '#B0174F', '#E0457E'), neu=('#EEECF4', '#5C5878', '#A09BB8'), warn=('#FFF1DA', '#8A4F00', '#E39A1F')),
   'dark': dict(info=('#262056', '#C9BEFF', '#9C86FF'), ok=('#10302A', '#7AE6C1', '#45D3A2'), err=('#371829', '#FFA3C1', '#FF7EA8'), neu=('#26223C', '#BDB7DA', '#8C86B3'), warn=('#33280F', '#F7CB78', '#F2B552'))}),
 ('rich', 'Насыщенная', 'Фон плотнее, текст темнее', {
   'light': dict(info=('#DCD6FF', '#2E1BA8', '#4B30E0'), ok=('#CBEFE2', '#075C47', '#0E8A6A'), err=('#F9D3E1', '#9C1243', '#D2306C'), neu=('#E3E0EC', '#4A4664', '#8E89A8'), warn=('#FFE3B3', '#7A4500', '#D88A0E')),
   'dark': dict(info=('#332A7A', '#DDD5FF', '#A38FFF'), ok=('#134238', '#93F2CF', '#45D3A2'), err=('#4D1D37', '#FFBDD2', '#FF7EA8'), neu=('#312C4C', '#D0CBE8', '#9A94C2'), warn=('#473611', '#FBD892', '#F2B552'))}),
 ('mono', 'Тёмный текст', 'Цветной фон и точка, текст один', {
   'light': dict(info=('#ECE9FF', '#1B1730', '#5B3FF0'), ok=('#E1F5EE', '#1B1730', '#14A57F'), err=('#FCE8EF', '#1B1730', '#E0457E'), neu=('#EEECF4', '#1B1730', '#A09BB8'), warn=('#FFF1DA', '#1B1730', '#E39A1F')),
   'dark': dict(info=('#262056', '#F5F3FF', '#9C86FF'), ok=('#10302A', '#F5F3FF', '#45D3A2'), err=('#371829', '#F5F3FF', '#FF7EA8'), neu=('#26223C', '#F5F3FF', '#8C86B3'), warn=('#33280F', '#F5F3FF', '#F2B552'))}),
 ('solid', 'Сплошная', 'Плотная заливка, белый текст', {
   'light': dict(info=('#4B30E0', '#FFFFFF', '#FFFFFF'), ok=('#0B7A5F', '#FFFFFF', '#FFFFFF'), err=('#C01F59', '#FFFFFF', '#FFFFFF'), neu=('#6E6989', '#FFFFFF', '#FFFFFF'), warn=('#9A5800', '#FFFFFF', '#FFFFFF')),
   'dark': dict(info=('#8C76FF', '#0D0B18', '#0D0B18'), ok=('#3CC896', '#06140F', '#06140F'), err=('#FF6F9C', '#1A0610', '#1A0610'), neu=('#8C86B3', '#0D0B18', '#0D0B18'), warn=('#F2B552', '#1D1400', '#1D1400'))}),
 ('text', 'Только текст', 'Без подложки, цвет в тексте', {
   'light': dict(info=(None, '#3B25C4', '#5B3FF0'), ok=(None, '#0A6B53', '#14A57F'), err=(None, '#B0174F', '#E0457E'), neu=(None, '#5C5878', '#A09BB8'), warn=(None, '#8A4F00', '#E39A1F')),
   'dark': dict(info=(None, '#C9BEFF', '#9C86FF'), ok=(None, '#7AE6C1', '#45D3A2'), err=(None, '#FFA3C1', '#FF7EA8'), neu=(None, '#BDB7DA', '#8C86B3'), warn=(None, '#F7CB78', '#F2B552'))}),
 ('gray', 'Серый фон', 'Подложка одна, цвет только в точке', {
   'light': dict(info=('#EEECF4', '#1B1730', '#5B3FF0'), ok=('#EEECF4', '#1B1730', '#14A57F'), err=('#EEECF4', '#1B1730', '#E0457E'), neu=('#EEECF4', '#5C5878', '#A09BB8'), warn=('#EEECF4', '#1B1730', '#E39A1F')),
   'dark': dict(info=('#26223C', '#F5F3FF', '#9C86FF'), ok=('#26223C', '#F5F3FF', '#45D3A2'), err=('#26223C', '#F5F3FF', '#FF7EA8'), neu=('#26223C', '#BDB7DA', '#8C86B3'), warn=('#26223C', '#F5F3FF', '#F2B552'))}),
]
SURF = {'light': '#FFFFFF', 'dark': '#171329'}


def lum(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)


def tag(label, bg, fg, dot, pulse=False):
    st = f'color:{fg};' + (f'background:{bg};' if bg else 'background:none;padding-left:0;padding-right:0;')
    return f'<span class="tag{" pl" if pulse else ""}" style="{st}--d:{dot}"><i></i>{label}</span>'


def table(mode):
    head = '<tr><th scope="col">Статус</th>' + ''.join(f'<th scope="col"><b>{n}</b><small>{d}</small></th>' for k, n, d, _ in V) + '</tr>'
    rows = ''
    worst = {}
    for label, role, note in ST:
        cells = ''
        for k, n, d, pal in V:
            bg, fg, dot = pal[mode][role]
            c = cr(fg, bg or SURF[mode])
            worst[k] = min(worst.get(k, 99), c)
            flag = ' low' if c < 4.5 else ''
            cells += f'<td>{tag(label, bg, fg, dot, role == "info")}<em class="c{flag}">{c:.1f}</em></td>'
        rows += f'<tr><th scope="row"><b>{label}</b><small>{note}</small></th>{cells}</tr>'
    foot = '<tr class="min"><th scope="row">Минимальный контраст</th>' + ''.join(f'<td>{worst[k]:.1f}</td>' for k, *_ in V) + '</tr>'
    return f'<div class="tw {mode}"><table><thead>{head}</thead><tbody>{rows}{foot}</tbody></table></div>', worst


lt, wl = table('light')
dk, wd = table('dark')

HTML = f'''<title>Libre.zone: статусы</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap">
<style>
/* Таблица статусов: все статусы × шесть вариантов цвета, светлая и тёмная тема на фиксированных подложках. */
:root{{--bg:#F5F3FB;--card:#FFFFFF;--t:#16122B;--t2:#5F5978;--line:#E9E5F4;--accent:#4B30E0;--fd:"Manrope","Inter",system-ui,sans-serif;--font:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0F0D1A;--card:#191628;--t:#F2F0FA;--t2:#A39DBD;--line:#2C2742;--accent:#A58BFF;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0F0D1A;--card:#191628;--t:#F2F0FA;--t2:#A39DBD;--line:#2C2742;--accent:#A58BFF;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--t);font-family:var(--font);font-size:15px;line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 72px}}
.wrap{{max-width:1320px;margin:0 auto;display:flex;flex-direction:column;gap:28px}}
.intro{{display:flex;flex-direction:column;gap:10px;max-width:780px}}
.eyebrow{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}}
h1{{font-family:var(--fd);font-size:clamp(28px,4vw,40px);line-height:1.1;margin:0;font-weight:800;text-wrap:balance}}
h2{{font-family:var(--fd);font-size:22px;margin:0}}
.intro p{{margin:0;color:var(--t2);max-width:72ch;text-wrap:pretty}}
section{{display:flex;flex-direction:column;gap:12px}}
.tw{{overflow-x:auto;border-radius:20px}}
.tw.light{{background:#FFFFFF;color:#1B1730;--rl:#EEEBF6;--s2:#6A6585}}
.tw.dark{{background:#171329;color:#F5F3FF;--rl:#2A2545;--s2:#A9A3C9}}
.tw.light th,.tw.light td{{color:#1B1730}}.tw.dark th,.tw.dark td{{color:#F5F3FF}}
table{{border-collapse:collapse;width:100%;min-width:980px}}
th,td{{padding:10px 10px;text-align:left;vertical-align:middle}}
tbody th{{width:150px}}
thead th{{vertical-align:bottom;padding-top:16px;padding-bottom:12px}}
thead th b{{display:block;font-family:var(--fd);font-size:14px}}
thead th small,tbody th small{{display:block;font-size:11.5px;line-height:15px;color:var(--s2);font-weight:400;max-width:180px}}
thead th:first-child{{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--s2);font-weight:600}}
tbody tr + tr th,tbody tr + tr td{{border-top:1px solid var(--rl)}}
tbody th b{{display:block;font-size:13.5px;font-weight:600}}
td{{white-space:nowrap}}
.tag{{display:inline-flex;align-items:center;gap:6px;padding:4px 10px 4px 9px;border-radius:999px;font-size:12px;line-height:16px;font-weight:600;letter-spacing:.005em}}
.tag i{{width:7px;height:7px;border-radius:50%;background:var(--d);flex:none}}
.tag.pl i{{box-shadow:0 0 0 3px color-mix(in srgb,var(--d) 25%,transparent)}}
em.c{{display:block;font-style:normal;font-size:10.5px;line-height:14px;color:var(--s2);margin-top:4px;font-variant-numeric:tabular-nums}}
em.c.low{{color:#E0457E;font-weight:600}}
tr.min th,tr.min td{{font-size:12px;color:var(--s2);font-variant-numeric:tabular-nums;font-weight:600}}
.legend{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}}
.legend div{{background:var(--card);border-radius:16px;padding:14px 16px;font-size:13.5px;color:var(--t2)}}
.legend b{{display:block;color:var(--t);margin-bottom:2px}}
</style>
<div class="wrap">
  <div class="intro">
    <span class="eyebrow">Libre.zone · статусы</span>
    <h1>Таблица статусов</h1>
    <p>Все 12 статусов прототипа в шести вариантах цвета текста и фона. Под каждой меткой контраст текста к фону: норма WCAG AA — 4,5, ниже неё значение подсвечено. Метки «в процессе» везде с мягким ореолом у точки.</p>
  </div>
  <div class="legend">
    <div><b>Процесс</b>Ожидание, проверки, отправка. Цвет бренда.</div>
    <div><b>Успех</b>Завершён, Открыто. Изумрудный.</div>
    <div><b>Ошибка</b>Ошибка. Малиновый.</div>
    <div><b>Нейтральный</b>Создан, Отменён, Закрыто. Серо-лавандовый.</div>
    <div><b>Внимание</b>Время на исходе. Янтарный.</div>
  </div>
  <section><h2>Светлая тема</h2>{lt}</section>
  <section><h2>Тёмная тема</h2>{dk}</section>
</div>
'''
open(OUT, 'w').write(HTML)
print('light', {k: round(v, 1) for k, v in wl.items()}); print('dark', {k: round(v, 1) for k, v in wd.items()})
