import json
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/'
sets=json.load(open(S+'ic2/sets.json')); cur=json.load(open(S+'ic.json'))
M=dict(swap='home',list='list',user='user',chev='chevd',arrow='arrow',check='check',checkc='checkc',close='close',copy='copy',search='search',clock='clock',warn='warn',lock='lock',shield='shield',bank='bank',gift='gift',logout='logout')
row={}
for k,v in M.items():
    if v in cur: row[k]='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'+cur[v]+'</svg>'
allsets={'Текущий (нарисован вручную)':row}; allsets.update(sets)
LAB=dict(swap='Обмен',list='Мои обмены',user='Профиль',chev='Раскрыть',arrow='Далее',check='Галочка',checkc='Успех',close='Закрыть',copy='Копировать',search='Поиск',clock='Время',warn='Внимание',lock='Замок',shield='Безопасность',bank='Банк',gift='Подарок',logout='Выйти')
NOTE={'Текущий (нарисован вручную)':'Тонкий штрих, угловатые концы; набор неполный и неровный по стилю.',
'Lucide':'Нейтральный линейный набор, штрих 1,5–2 px. Самый «безопасный» вариант.',
'Phosphor Regular':'Линейный, чуть мягче и круглее Lucide, больше характера.',
'Phosphor Duotone':'Тот же Phosphor с полупрозрачной заливкой — живее, но тяжелее.',
'Solar Linear':'Дружелюбный, скруглённый, современный «финтех»-стиль.',
'Solar Duotone':'Solar с полутоновой заливкой — заметно выразительнее.',
'Iconoir':'Тонкий и аккуратный, чуть «редакционный», много воздуха.',
'Remix Line':'Плотный, геометричный, чёткий; хорошо читается мелко.',
'Mingcute Line':'Мягкие углы, лёгкая округлость, дружелюбный.',
'Hugeicons':'Тонкий, скруглённый, современный; много финансовых иконок.'}
out=''
for n,r in allsets.items():
    cells=''.join(f'<div class="c"><span class="i">{r[k]}</span><small>{LAB[k]}</small></div>' for k in M if k in r)
    tab=''.join(f'<div class="tb{" on" if i==0 else ""}"><span class="i">{r[k]}</span><small>{t}</small></div>' for i,(k,t) in enumerate([('swap','Обмен'),('list','Мои обмены'),('user','Профиль')]))
    why=''.join(f'<div class="why"><span class="ci">{r[k]}</span><div><b>{t}</b><small>{s}</small></div></div>' for k,t,s in [('shield','Безопасно','Без документов'),('bank','СБП','Любой банк')])
    st=f'<div class="ok"><span class="i">{r["checkc"]}</span>Обмен завершён</div><div class="rw"><span class="i">{r["clock"]}</span>Осталось на оплату<b>09:12</b></div><div class="rw"><span class="i">{r["copy"]}</span>Скопировать номер<span class="i r">{r["arrow"]}</span></div>'
    out+=f'<section class="set"><div class="hd"><h2>{n}</h2><p>{NOTE[n]}</p></div><div class="grid">{cells}</div><div class="ui"><div class="card">{st}</div><div class="card">{why}</div><div class="bar">{tab}</div></div></section>'
html='''<title>Наборы иконок — сравнение</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<style>
:root{--bg:#F6F4FC;--fg:#1B1730;--mut:#5C5878;--card:#fff;--line:#E5E1F3;--ac:#6535F5;--soft:#EEE8FF;--ok:#0B7A5F}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0D0B18;--fg:#F5F3FF;--mut:#B6B0D6;--card:#171329;--line:#2B2549;--ac:#B49CFF;--soft:#241D47;--ok:#45D3A2;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0D0B18;--fg:#F5F3FF;--mut:#B6B0D6;--card:#171329;--line:#2B2549;--ac:#B49CFF;--soft:#241D47;--ok:#45D3A2;color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/20px Manrope,system-ui,sans-serif;padding-block:24px;padding-inline:16px}
.w{max-width:1100px;margin:0 auto}h1{font-size:22px;line-height:28px;margin:0 0 6px}.lead{color:var(--mut);margin:0 0 24px;max-width:70ch}
.set{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:18px;margin-bottom:16px;display:grid;gap:14px;min-width:0}
.hd h2{font-size:17px;margin:0}.hd p{margin:2px 0 0;color:var(--mut);font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(84px,1fr));gap:6px}
.c{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 4px;border-radius:12px;background:var(--bg)}
.c small{font-size:11px;line-height:14px;color:var(--mut);text-align:center}
.i{display:inline-grid;place-items:center;width:24px;height:24px;color:var(--fg)}.i svg{width:24px;height:24px;display:block}
.ui{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.card{background:var(--bg);border-radius:16px;padding:6px 12px;display:flex;flex-direction:column}
.ok{display:flex;align-items:center;gap:10px;font-weight:700;padding:10px 0}.ok .i{color:var(--ok)}
.rw{display:flex;align-items:center;gap:10px;padding:10px 0;border-top:1px solid var(--line);font-size:13px}.rw .i{color:var(--mut)}.rw b{margin-left:auto;color:var(--fg)}.rw .r{margin-left:auto}
.why{display:flex;align-items:center;gap:12px;padding:10px 0}.why+.why{border-top:1px solid var(--line)}.why .ci{width:40px;height:40px;border-radius:12px;background:var(--soft);display:grid;place-items:center;color:var(--ac);flex:none}.why b{display:block;font-size:14px}.why small{color:var(--mut);font-size:12px}
.bar{display:flex;justify-content:space-around;align-items:center;background:var(--bg);border-radius:16px;padding:8px 6px}
.tb{display:flex;flex-direction:column;align-items:center;gap:2px;color:var(--mut)}.tb .i{color:inherit}.tb small{font-size:11px}.tb.on{color:var(--ac)}
</style>
<div class="w"><h1>Наборы иконок — сравнение</h1>
<p class="lead">Те же 17 иконок интерфейса в разных наборах: сетка с подписями и мини-превью (итог обмена, «Почему Libre.zone», таб-бар). Первый ряд — то, что сейчас в прототипе. Смотрите на характер штриха, скругления и читаемость на 24 px.</p>
'''+out+'</div>'
open(S+'libre-zone-icon-sets.html','w').write(html)
