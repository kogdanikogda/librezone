#!/usr/bin/env python3
# Генерирует доску вариантов формы обмена Libre.zone (статичный HTML)
OUT = '/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/libre-zone-form-variants.html'

AMTS = [50, 100, 1000, 5000, 10000, 50000]
RATE = 82.91
# мок-данные ликвидности: заявок, минут, уровень 1..3
LIQ = {50: (18, 2, 3), 100: (24, 2, 3), 1000: (11, 4, 3), 5000: (2, 20, 1), 10000: (5, 8, 2), 50000: (1, 35, 1)}


def rub(n):
    return f"{n:,}".replace(',', ' ') + ' ₽'


def usdt(n):
    v = n / RATE
    s = f"{v:,.2f}".replace(',', ' ').replace('.', ',').replace(' ', ' ')
    return s


def bars(lvl):
    return '<span class="bars">' + ''.join(f'<i class="{"on" if i < lvl else ""}"></i>' for i in range(3)) + '</span>'


def plural(n):
    if n % 10 == 1 and n % 100 != 11:
        return 'заявка'
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return 'заявки'
    return 'заявок'


ICON_SWAP = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4v16M7 4 3 8M7 4l4 4M17 20V4m0 16-4-4m4 4 4-4"/></svg>'
CHEV = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>'
CHEVR = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6 6 6-6 6"/></svg>'
CHECK = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>'
BOLT = '<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>'
CLOCK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
REPEAT = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/></svg>'

USDT_MARK = '<span class="cmark usdt">T</span>'
COINS = [('USDT', 'TRX', 'usdt', 'T'), ('BTC', 'Bitcoin', 'btc', '₿'), ('ETH', 'ERC-20', 'eth', 'Ξ'), ('TON', 'TON', 'ton', '◆')]


def rub_pill():
    return '<span class="curpill"><span class="rubmark">₽</span>RUB</span>'


def coin_pill(empty=False):
    if empty:
        return f'<span class="curpill empty">Выберите валюту {CHEV}</span>'
    return f'<span class="curpill">{USDT_MARK}<span>USDT<small>TRX</small></span>{CHEV}</span>'


def chips_default(sel=None):
    out = []
    for a in AMTS:
        p = 'true' if a == sel else 'false'
        out.append(f'<span class="chip" aria-pressed="{p}">{rub(a)}{bars(LIQ[a][2])}</span>')
    return '<div class="chips6">' + ''.join(out) + '</div>'


def calc_classic(state):
    """state: full | empty | coin"""
    full = state == 'full'
    give = '5 000' if full else '<span class="ph">0</span>'
    get = '60,30' if full else '<span class="ph">0</span>'
    rows = f'''
    <div class="crow"><div><div class="lbl">Отдаю</div><div class="big">{give}</div></div>{rub_pill()}</div>
    <div class="divider"><span class="swapbtn">{ICON_SWAP}</span></div>
    <div class="crow"><div><div class="lbl">Получаю</div><div class="big">{get}</div></div>{coin_pill(empty=(state == 'empty'))}</div>
    <div class="clabel"><span>Сумма в рублях</span><span>Чем больше столбиков, тем быстрее</span></div>
    {chips_default(5000 if full else None)}'''
    if full:
        eta = f'<div class="eta">{bars(1)}<div><b>≈ 20 мин</b>Встречных заявок мало, придётся подождать</div></div>'
        rate = f'<div class="rateline"><span>Курс <b>1 USDT = 82,91 ₽</b></span><span class="badge">{CHECK} с комиссией</span></div>'
        btn = '<span class="btn calcbtn">Продолжить</span>'
    elif state == 'coin':
        eta = f'<div class="eta hint">{CLOCK}<div><b>Выберите сумму</b>Покажем, сколько USDT получите и сколько ждать</div></div>'
        rate = f'<div class="rateline"><span>Курс <b>1 USDT = 82,91 ₽</b></span><span class="badge">{CHECK} с комиссией</span></div>'
        btn = '<span class="btn calcbtn dis">Выберите сумму</span>'
    else:
        eta = f'<div class="eta hint">{CLOCK}<div><b>Выберите валюту и сумму</b>Здесь появятся итог и время обмена</div></div>'
        rate = '<div class="rateline"><span>Курс появится после выбора валюты</span></div>'
        btn = '<span class="btn calcbtn dis">Выберите валюту</span>'
    return f'<div class="calc">{rows}{eta}{rate}{btn}</div>'


def seg():
    return '<div class="seg"><span class="on">Купить</span><span>Продать</span></div>'


def coin_tabs(sel='USDT'):
    out = []
    for c, net, k, m in COINS:
        on = ' on' if c == sel else ''
        out.append(f'<span class="ctab{on}"><span class="cmark {k}">{m}</span>{c}</span>')
    return '<div class="ctabs">' + ''.join(out) + '</div>'


def calc_result_chips():
    chips = []
    for a in AMTS:
        n, mins, lvl = LIQ[a]
        p = 'true' if a == 10000 else 'false'
        slow = ' slow' if lvl == 1 else ''
        chips.append(f'<span class="rchip{slow}" aria-pressed="{p}"><b>{rub(a)}</b><span class="get">{usdt(a)} USDT</span><span class="t">{CLOCK}≈ {mins} мин</span></span>')
    return f'''<div class="calc">{seg()}{coin_tabs()}
    <div class="clabel"><span>Сколько рублей отдаёте</span><span>курс 82,91 ₽</span></div>
    <div class="rgrid">{''.join(chips)}</div>
    <div class="rateline"><span>Получите <b>120,61 USDT</b></span><span class="badge">{CHECK} с комиссией</span></div>
    <span class="btn calcbtn">Продолжить</span></div>'''


def calc_pricelist():
    rows = []
    for a in AMTS:
        n, mins, lvl = LIQ[a]
        on = ' on' if a == 1000 else ''
        rows.append(f'<span class="prow{on}"><b>{rub(a)}</b><span class="get">→ {usdt(a)} USDT</span><span class="t">≈ {mins} мин</span>{CHEVR}</span>')
    return f'''<div class="calc">{seg()}
    <div class="crow tight"><div class="lbl">Покупаете</div>{coin_pill()}</div>
    <div class="plist">{''.join(rows)}</div>
    <div class="rateline"><span>Курс <b>1 USDT = 82,91 ₽</b></span><span class="badge">{CHECK} с комиссией</span></div>
    <span class="btn calcbtn">Купить 12,06 USDT за 1 000 ₽</span></div>'''


def calc_returning():
    return f'''<div class="calc">
    <div class="lbl">С возвращением, Иван</div>
    <div class="repeat">
      <div class="rhead"><span class="lbl">Последний обмен, 12.10</span><span class="badge">{CHECK} успешно</span></div>
      <div class="rpair"><div><span>Отдали</span><b>10 000 ₽</b></div><span class="arrow">→</span><div><span>Получите сейчас</span><b>120,61 USDT</b></div></div>
      <div class="rmeta">Т-Банк · TQn9…4xFz · ≈ 8 мин</div>
      <span class="btn calcbtn">{REPEAT}Повторить обмен</span>
    </div>
    <div class="clabel"><span>Или другая сумма</span><span>USDT · TRX</span></div>
    {chips_default(None)}
    <span class="btn ghost">Другая валюта или продажа</span></div>'''


FORM_VARIANTS = [
    ('A', 'Предвыбрано', 'Сейчас в прототипе', calc_classic('full'),
     'Сразу выбраны RUB → USDT и 5 000 ₽. Курс, итог и время видны с первого экрана, кнопка всегда активна.',
     ['Ноль действий до первого результата', 'Форма сразу выглядит «живой» — хорошо для портфолио'],
     ['Сумму выбрали за пользователя: можно не заметить и пройти дальше с чужим выбором', 'Неочевидно, что сумма — главный выбор']),
    ('B', 'Пустая форма', 'Ничего не выбрано', calc_classic('empty'),
     'Валюта и сумма не выбраны. Слоты итога, времени и курса заняты подсказками, поэтому высота такая же, как у заполненной формы.',
     ['Пользователь осознанно делает каждый выбор', 'Честно: ничего не навязываем'],
     ['Два обязательных действия до первой цифры', 'Пустые нули выглядят как «сломалось»', 'Курс не виден — главный аргумент сервиса спрятан']),
    ('C', 'Только валюта', 'Пара выбрана, сумма нет', calc_classic('coin'),
     'Выбрана самая популярная пара RUB → USDT, сумма — нет. Курс виден сразу, итог и время появляются после нажатия на сумму.',
     ['Один осознанный выбор — сумма', 'Курс виден с первого экрана', 'Высота не меняется'],
     ['Нули в полях ввода всё ещё выглядят пусто — можно заменить на «—»']),
    ('D', 'Итог в кнопке', 'Сумма = готовое предложение', calc_result_chips(),
     'Убираем поля «Отдаю/Получаю». Каждая кнопка — готовое предложение: сколько отдаёте, сколько получите и сколько ждать. Валюта — вкладки, без шторки.',
     ['Сравнить все суммы можно одним взглядом', 'Нет поля, которое «прыгает» при выборе', 'Валюта меняется в одно касание'],
     ['Больше текста в кнопках', 'Вкладки вмещают 4–5 монет; при росте списка нужна шторка']),
    ('E', 'Прайс-лист', 'Список вместо калькулятора', calc_pricelist(),
     'Раз суммы фиксированные, форма по сути — прайс-лист. Строка: сумма, итог, время. Кнопка внизу повторяет выбор целиком.',
     ['Самый понятный формат для фиксированных сумм', 'Легко добавить ещё суммы', 'Кнопка подтверждает выбор словами'],
     ['Меньше «вау» в hero', 'Длиннее по высоте, если сумм станет больше 6']),
    ('F', 'Для вернувшихся', 'Повтор последнего обмена', calc_returning(),
     'Для пользователя с историей: первый блок — повтор последнего обмена по текущему курсу. Ниже — быстрый выбор другой суммы.',
     ['Повторный обмен в одно касание', 'Реквизиты уже сохранены'],
     ['Только для вошедших; новичку нужен один из вариантов A–E']),
]

# ---------- кнопки сумм ----------


def grid(fn, sel=5000):
    return '<div class="chips6">' + ''.join(fn(a, a == sel) for a in AMTS) + '</div>'


def c_bars(a, s):
    return f'<span class="chip" aria-pressed="{str(s).lower()}">{rub(a)}{bars(LIQ[a][2])}</span>'


def c_count(a, s):
    n = LIQ[a][0]
    return f'<span class="chip" aria-pressed="{str(s).lower()}">{rub(a)}<small>{n} {plural(n)}</small></span>'


def c_time(a, s):
    m = LIQ[a][1]
    cls = ' slow' if LIQ[a][2] == 1 else ''
    return f'<span class="chip{cls}" aria-pressed="{str(s).lower()}">{rub(a)}<small>{CLOCK}≈ {m} мин</small></span>'


def c_meter(a, s):
    lvl = LIQ[a][2]
    w = {1: 22, 2: 58, 3: 100}[lvl]
    return f'<span class="chip meter" aria-pressed="{str(s).lower()}">{rub(a)}<span class="mbar"><i style="width:{w}%"></i></span></span>'


def c_words(a, s):
    lvl = LIQ[a][2]
    word = {1: 'долго', 2: 'средне', 3: 'быстро'}[lvl]
    dots = ''.join(f'<i class="{"on" if i < lvl else ""}"></i>' for i in range(3))
    return f'<span class="chip" aria-pressed="{str(s).lower()}">{rub(a)}<small class="words"><span class="dots">{dots}</span>{word}</small></span>'


def c_flag(a, s):
    lvl = LIQ[a][2]
    tag = f'<span class="flag">{BOLT}быстро</span>' if lvl == 3 else ''
    slow = ' slow' if lvl == 1 else ''
    return f'<span class="chip{slow}" aria-pressed="{str(s).lower()}">{tag}{rub(a)}</span>'


CHIP_VARIANTS = [
    ('1', 'Столбики', 'Сейчас в прототипе', grid(c_bars),
     'Три столбика как сигнал сети. Компактно, но требует подписи «чем больше столбиков, тем быстрее».', 'Нужна легенда'),
    ('2', 'Число заявок', 'Точная цифра', grid(c_count),
     'Показываем, сколько встречных заявок сейчас в очереди. Прозрачно, но пользователю цифра мало что говорит: «2 заявки» — это плохо или нормально?', 'Цифра без смысла для пользователя'),
    ('3', 'Время ожидания', 'Ответ на вопрос «сколько ждать»', grid(c_time),
     'Переводим заявки в минуты — именно это волнует пользователя. Медленные суммы приглушены текстом, а не только цветом.', 'Рекомендую'),
    ('4', 'Шкала', 'Уровень заполнения', grid(c_meter),
     'Тонкая полоса внизу кнопки. Читается быстрее столбиков, но без цифр — тоже нужна легенда.', 'Красиво, но абстрактно'),
    ('5', 'Слово + точки', 'Быстро · средне · долго', grid(c_words),
     'Три градации словами. Понятно без легенды, работает для дальтоников и в тёмной теме.', 'Простой и надёжный'),
    ('6', 'Метка «быстро»', 'Подсвечиваем только лучшее', grid(c_flag),
     'Метка только на суммах с высокой ликвидностью, остальные чистые. Минимум шума, подталкивает к быстрым суммам.', 'Минимализм, меньше информации'),
]


def tags(pros, cons):
    p = ''.join(f'<li>{x}</li>' for x in pros)
    c = ''.join(f'<li>{x}</li>' for x in cons)
    return f'<div class="pc"><div><h4 class="plus">Плюсы</h4><ul>{p}</ul></div><div><h4 class="minus">Минусы</h4><ul>{c}</ul></div></div>'


form_cards = ''.join(f'''
<article class="card" id="form-{k}">
  <header><span class="key">{k}</span><div><h3>{t}</h3><p class="sub">{st}</p></div></header>
  <div class="stage">{mock}</div>
  <p class="desc">{d}</p>
  {tags(pr, co)}
</article>''' for k, t, st, mock, d, pr, co in FORM_VARIANTS)

chip_cards = ''.join(f'''
<article class="card chipcard{' rec' if v == 'Рекомендую' else ''}" id="chip-{k}">
  <header><span class="key">{k}</span><div><h3>{t}</h3><p class="sub">{st}</p></div></header>
  <span class="verdict">{v}</span>
  <div class="stage strip">{mock}</div>
  <p class="desc">{d}</p>
</article>''' for k, t, st, mock, d, v in CHIP_VARIANTS)

HTML = f'''<title>Форма обмена: варианты</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap">
<style>
/* Доска сравнения: вариант = карточка с макетом формы в стиле Aurora + плюсы/минусы. */
:root{{
  --bg:#F5F3FB; --surface:#FFFFFF; --text:#16122B; --text2:#5F5978; --line:#E4DFF2;
  --accent:#5A34E8; --good:#14804A; --bad:#C2352B; --keybg:#16122B; --keyfg:#FFFFFF;
  --rec:#EDE7FF;
  --grad:linear-gradient(135deg,#4F2BFF,#8349FF 55%,#D447D6);
  --fd:"Manrope","Inter",system-ui,sans-serif; --font:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --bg:#0F0D1A; --surface:#191628; --text:#F2F0FA; --text2:#A39DBD; --line:#2C2742;
  --accent:#A58BFF; --good:#4CD38A; --bad:#FF7F73; --keybg:#F2F0FA; --keyfg:#16122B; --rec:#241D44; color-scheme:dark}}}}
:root[data-theme="dark"]{{
  --bg:#0F0D1A; --surface:#191628; --text:#F2F0FA; --text2:#A39DBD; --line:#2C2742;
  --accent:#A58BFF; --good:#4CD38A; --bad:#FF7F73; --keybg:#F2F0FA; --keyfg:#16122B; --rec:#241D44; color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:var(--font);font-size:15px;line-height:1.5;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 64px}}
.wrap{{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:48px}}
.intro{{display:flex;flex-direction:column;gap:10px;max-width:720px}}
.eyebrow{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}}
h1{{font-family:var(--fd);font-size:clamp(28px,4vw,40px);line-height:1.1;margin:0;text-wrap:balance;font-weight:800}}
h2{{font-family:var(--fd);font-size:24px;line-height:1.2;margin:0;text-wrap:balance;font-weight:800}}
.intro p,.sec-head p{{margin:0;color:var(--text2);max-width:66ch}}
section{{display:flex;flex-direction:column;gap:20px}}
.sec-head{{display:flex;flex-direction:column;gap:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:20px}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:18px;display:flex;flex-direction:column;gap:14px;min-width:0}}
.card header{{display:flex;align-items:flex-start;gap:12px}}
.card h3{{margin:0;font-family:var(--fd);font-size:18px;line-height:1.25;font-weight:700}}
.sub{{margin:2px 0 0;font-size:13px;color:var(--text2)}}
.key{{flex:none;width:30px;height:30px;border-radius:9px;background:var(--keybg);color:var(--keyfg);display:grid;place-items:center;font-family:var(--fd);font-weight:800;font-size:15px}}
.verdict{{align-self:flex-start;margin-top:-4px;font-size:12px;line-height:16px;padding:4px 10px;border-radius:999px;border:1px solid var(--line);color:var(--text2);white-space:nowrap}}
.chipcard.rec{{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent) inset}}
.chipcard.rec .verdict{{background:var(--accent);color:var(--surface);border-color:transparent;font-weight:600}}
.desc{{margin:0;font-size:14px;color:var(--text2)}}
.pc{{display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:13px;line-height:1.45}}
.pc h4{{margin:0 0 4px;font-size:12px;letter-spacing:.06em;text-transform:uppercase}}
.pc .plus{{color:var(--good)}} .pc .minus{{color:var(--bad)}}
.pc ul{{margin:0;padding-left:16px;display:flex;flex-direction:column;gap:3px}}
.stage{{display:flex;justify-content:center;padding:14px;border-radius:16px;background:var(--bg)}}
.stage.strip{{padding:0;background:none}}
.stage.strip .chips6{{width:100%;padding:14px;border-radius:16px;background:var(--grad)}}

/* ----- макет формы (Aurora, фиксированная палитра поверхности) ----- */
.calc{{width:100%;max-width:330px;height:540px;background:var(--grad);color:#fff;border-radius:22px;padding:16px;display:flex;flex-direction:column;gap:11px;
  box-shadow:0 18px 40px -18px rgba(79,43,255,.55);position:relative;overflow:hidden;
  --f:rgba(255,255,255,.16);--l:rgba(255,255,255,.30);--on2:rgba(255,255,255,.80);--cb:#FFFFFF;--ocb:#4F2BFF}}
.calc::before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.22) 1px,transparent 1.2px);background-size:14px 14px;
  -webkit-mask-image:linear-gradient(160deg,transparent 45%,#000);mask-image:linear-gradient(160deg,transparent 45%,#000);pointer-events:none}}
.calc>*{{position:relative;flex:none}}
.lbl{{font-size:12px;line-height:16px;color:var(--on2);letter-spacing:.02em}}
.crow{{display:flex;align-items:center;justify-content:space-between;gap:10px}}
.crow.tight .lbl{{font-size:13px}}
.big{{font-family:var(--fd);font-size:28px;line-height:34px;font-weight:700;font-variant-numeric:tabular-nums}}
.ph{{opacity:.45}}
.curpill{{display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 12px 0 9px;border-radius:999px;border:1px solid var(--l);background:var(--f);font-size:14px;font-weight:600;line-height:15px;white-space:nowrap}}
.curpill small{{display:block;font-size:10.5px;font-weight:400;color:var(--on2);line-height:12px}}
.curpill.empty{{border-style:dashed;padding:0 12px 0 14px;font-weight:500}}
.rubmark,.cmark{{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-size:13px;font-weight:700;flex:none}}
.rubmark{{background:#fff;color:#4F2BFF}}
.cmark.usdt{{background:#E8222E;color:#fff}} .cmark.btc{{background:#F7931A;color:#fff}} .cmark.eth{{background:#3C3C3D;color:#fff}} .cmark.ton{{background:#0098EA;color:#fff;font-size:11px}}
.divider{{height:1px;background:var(--l);margin:3px 0}}
.swapbtn{{position:absolute;left:calc(50% - 20px);top:-20px;width:40px;height:40px;border-radius:50%;border:1px solid var(--l);background:#7a3ff0;display:grid;place-items:center}}
.clabel{{font-size:11.5px;line-height:15px;color:var(--on2);display:flex;justify-content:space-between;gap:8px}}
.chips6{{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}}
.chip{{position:relative;height:52px;border-radius:13px;border:1px solid var(--l,rgba(255,255,255,.3));background:var(--f,rgba(255,255,255,.16));color:#fff;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:600;line-height:17px;font-variant-numeric:tabular-nums;white-space:nowrap}}
.chip small{{display:inline-flex;align-items:center;gap:4px;font-size:11px;line-height:13px;font-weight:500;opacity:.85}}
.chip[aria-pressed="true"]{{background:#fff;color:#4F2BFF;border-color:transparent}}
.chip.slow{{border-style:dashed}}
.chip.slow small{{opacity:.7}}
.chip.meter{{justify-content:center;padding-bottom:4px}}
.mbar{{position:absolute;left:10px;right:10px;bottom:7px;height:3px;border-radius:2px;background:currentColor;opacity:.9;overflow:hidden}}
.mbar{{background:rgba(255,255,255,.25)}}
.chip[aria-pressed="true"] .mbar{{background:rgba(79,43,255,.18)}}
.mbar i{{display:block;height:100%;background:currentColor;border-radius:2px}}
.chip .words{{text-transform:lowercase}}
.dots{{display:inline-flex;gap:2px}} .dots i{{width:5px;height:5px;border-radius:50%;background:currentColor;opacity:.3;display:block}} .dots i.on{{opacity:1}}
.flag{{position:absolute;top:-7px;right:6px;display:inline-flex;align-items:center;gap:2px;padding:1px 6px;border-radius:999px;background:#FFE15A;color:#2A1A00;font-size:10px;line-height:14px;font-weight:700}}
.bars{{display:inline-flex;gap:2px;align-items:flex-end;height:10px}}
.bars i{{width:4px;border-radius:1px;background:currentColor;opacity:.3;display:block}}
.bars i:nth-child(1){{height:4px}}.bars i:nth-child(2){{height:7px}}.bars i:nth-child(3){{height:10px}}
.bars i.on{{opacity:1}}
.eta{{display:flex;align-items:center;gap:10px;min-height:54px;padding:8px 12px;border-radius:13px;background:var(--f);font-size:12px;line-height:16px;color:var(--on2)}}
.eta b{{color:#fff;font-size:14px;line-height:18px;display:block}}
.eta .bars{{color:#fff;transform:scale(1.2);margin:0 4px}}
.eta.hint{{border:1px dashed var(--l);background:transparent}}
.eta.hint svg{{flex:none;width:20px;height:20px;margin:0 2px;color:#fff}}
.rateline{{display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:12.5px;line-height:18px;color:var(--on2);min-height:22px}}
.rateline b{{color:#fff;font-weight:600}}
.rateline>span:first-child{{white-space:nowrap}}
.clabel span:first-child{{white-space:nowrap}}
.badge{{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:999px;background:var(--f);font-size:10.5px;line-height:16px;color:#fff;white-space:nowrap}}
.btn{{margin-top:auto;height:52px;border-radius:14px;display:flex;align-items:center;justify-content:center;gap:8px;font-weight:600;font-size:15px}}
.btn.calcbtn{{background:var(--cb);color:var(--ocb)}}
.btn.calcbtn.dis{{background:var(--f);color:var(--on2)}}
.btn.ghost{{margin-top:0;height:44px;border:1px solid var(--l);color:#fff;font-size:14px;font-weight:500}}
/* сегмент + вкладки монет */
.seg{{display:grid;grid-template-columns:1fr 1fr;padding:4px;border-radius:13px;background:rgba(20,8,70,.22);font-size:14px;font-weight:600}}
.seg span{{height:36px;display:grid;place-items:center;border-radius:10px;color:var(--on2)}}
.seg .on{{background:#fff;color:#4F2BFF}}
.ctabs{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}}
.ctab{{height:40px;border-radius:12px;border:1px solid var(--l);display:flex;align-items:center;justify-content:center;gap:6px;font-size:13px;font-weight:600}}
.ctab .cmark{{width:18px;height:18px;font-size:10px}}
.ctab.on{{background:var(--f);border-color:#fff;box-shadow:0 0 0 1px #fff inset}}
.rgrid{{display:grid;grid-template-columns:1fr 1fr;gap:7px}}
.rchip{{height:74px;border-radius:13px;border:1px solid var(--l);background:var(--f);padding:8px 10px;display:flex;flex-direction:column;justify-content:center;gap:1px;font-variant-numeric:tabular-nums}}
.rchip b{{font-size:15px;line-height:19px}}
.rchip .get{{font-size:12px;line-height:16px;color:var(--on2)}}
.rchip .t{{display:inline-flex;align-items:center;gap:4px;font-size:11px;line-height:14px;color:var(--on2)}}
.rchip.slow{{border-style:dashed}}
.rchip[aria-pressed="true"]{{background:#fff;color:#4F2BFF;border-color:transparent}}
.rchip[aria-pressed="true"] .get,.rchip[aria-pressed="true"] .t{{color:#5B48B8}}
/* прайс-лист */
.plist{{display:flex;flex-direction:column;border-radius:14px;overflow:hidden;border:1px solid var(--l)}}
.prow{{display:grid;grid-template-columns:70px 1fr auto 14px;align-items:center;gap:6px;height:44px;padding:0 10px 0 12px;font-size:13px;font-variant-numeric:tabular-nums;border-top:1px solid var(--l)}}
.prow:first-child{{border-top:0}}
.prow b{{font-size:14px;white-space:nowrap}}
.prow .get{{white-space:nowrap}}
.prow .arrow{{color:var(--on2)}}
.prow .t{{font-size:11.5px;color:var(--on2);white-space:nowrap}}
.prow svg{{color:var(--on2)}}
.prow.on{{background:#fff;color:#4F2BFF}}
.prow.on .arrow,.prow.on .t,.prow.on svg{{color:#5B48B8}}
/* повтор */
.repeat{{border-radius:16px;background:rgba(255,255,255,.14);border:1px solid var(--l);padding:12px;display:flex;flex-direction:column;gap:10px}}
.rhead{{display:flex;justify-content:space-between;align-items:center;gap:8px}}
.rpair{{display:flex;align-items:center;gap:10px}}
.rpair div{{display:flex;flex-direction:column}}
.rpair span{{font-size:11.5px;color:var(--on2)}}
.rpair b{{font-family:var(--fd);font-size:19px;line-height:26px;white-space:nowrap}}
.rpair .arrow{{font-size:18px;color:var(--on2)}}
.rmeta{{font-size:12px;color:var(--on2)}}
.repeat .btn{{margin-top:0;height:46px}}

.reco{{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:22px;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}}
.reco h3{{margin:0 0 6px;font-family:var(--fd);font-size:17px}}
.reco p{{margin:0;color:var(--text2);font-size:14px}}
.reco b{{color:var(--text)}}
@media (max-width:420px){{.grid{{grid-template-columns:1fr}} .pc{{grid-template-columns:1fr}} .chip{{font-size:13px}}}}
</style>

<div class="wrap">
  <div class="intro">
    <span class="eyebrow">Libre.zone · форма обмена · Aurora</span>
    <h1>Как показать форму при первом открытии</h1>
    <p>Шесть вариантов стартового состояния и шесть способов показать, сколько встречных заявок у каждой суммы. Все формы одной высоты: при выборе пары и суммы ничего не прыгает. Данные заявок условные.</p>
  </div>

  <section>
    <div class="sec-head"><h2>Стартовое состояние формы</h2>
      <p>A–C — тот же калькулятор с разной степенью предвыбора. D–F — другая компоновка той же задачи.</p></div>
    <div class="grid">{form_cards}</div>
  </section>

  <section>
    <div class="sec-head"><h2>Заявки в кнопках сумм</h2>
      <p>Пользователю важно не количество заявок, а сколько ждать. Медленные суммы везде отмечены не только цветом: пунктиром, словом или временем.</p></div>
    <div class="grid">{chip_cards}</div>
  </section>

  <section>
    <div class="sec-head"><h2>Что я бы выбрал</h2></div>
    <div class="reco">
      <div><h3>Форма: C или D</h3><p><b>C «Только валюта»</b> — минимальное изменение текущего дизайна: курс виден сразу, сумму пользователь выбирает сам. <b>D «Итог в кнопке»</b> — смелее и лучше для кейса: убирает поля, которые меняются, и показывает все предложения сразу.</p></div>
      <div><h3>Кнопки: время ожидания</h3><p><b>Вариант 3</b> отвечает на настоящий вопрос пользователя и не требует легенды. Если места мало — <b>вариант 5</b> «слово + точки».</p></div>
      <div><h3>Плюс к любому варианту</h3><p><b>F «Для вернувшихся»</b> подключается поверх выбранной формы, когда у пользователя есть история обменов.</p></div>
    </div>
  </section>
</div>
'''

open(OUT, 'w').write(HTML)
print('ok', len(HTML))
