import re, json, os
S='/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/'
R=S+'icons/node_modules/'
IC=json.load(open(S+'ic.json'))
# project name -> (label, where used, lucide, tabler, hero, phosphor)
W=[
('home','Обмен','таб-бар, вкладка',['arrow-left-right','arrow-left-right','arrows-right-left','arrows-left-right']),
('list','Мои обмены','таб-бар',['list','list','list-bullet','list']),
('user','Профиль','таб-бар',['user','user','user','user']),
('swapv','Поменять местами','форма обмена',['arrow-up-down','arrows-up-down','arrows-up-down','arrows-down-up']),
('chevd','Раскрыть','селекторы, шторки',['chevron-down','chevron-down','chevron-down','caret-down']),
('chevl','Назад','шапка',['chevron-left','chevron-left','chevron-left','caret-left']),
('arrow','Далее','кнопки, строки',['arrow-right','arrow-right','arrow-right','arrow-right']),
('check','Галочка','степпер, чекбоксы',['check','check','check','check']),
('checkc','Успех','итог обмена, статусы',['circle-check','circle-check','check-circle','check-circle']),
('closec','Ошибка / отмена','итог обмена, статусы',['circle-x','circle-x','x-circle','x-circle']),
('close','Закрыть','шторки, модалки',['x','x','x-mark','x']),
('copy','Копировать','номер заявки, адрес',['copy','copy','clipboard-document','copy']),
('ext','Открыть ссылку','партнёры, документы',['external-link','external-link','arrow-top-right-on-square','arrow-square-out']),
('redo','Повторить обмен','история',['rotate-cw','rotate-clockwise','arrow-path','arrow-clockwise']),
('search','Поиск','выбор валюты',['search','search','magnifying-glass','magnifying-glass']),
('clock','Время','таймер, ожидание',['clock','clock','clock','clock']),
('info','Информация','подсказки, плашки',['info','info-circle','information-circle','info']),
('warn','Внимание','предупреждения',['triangle-alert','alert-triangle','exclamation-triangle','warning']),
('lock','Нельзя изменить','профиль: email, телефон',['lock','lock','lock-closed','lock']),
('doc','Документ','правила и политика',['file-text','file-text','document-text','file-text']),
('mail','Почта','профиль, помощь',['mail','mail','envelope','envelope-simple']),
('send','Telegram / связь','помощь',['send','send','paper-airplane','paper-plane-tilt']),
('bell','Уведомления','настройки',['bell','bell','bell','bell']),
('globe','Язык','настройки',['globe','world','globe-alt','globe']),
('sun','Светлая тема','настройки',['sun','sun','sun','sun']),
('moon','Тёмная тема','настройки',['moon','moon','moon','moon']),
('logout','Выйти','профиль',['log-out','logout','arrow-right-start-on-rectangle','sign-out']),
('chart','Курс фиксируется','«Почему Libre.zone»',['chart-line','chart-line','chart-bar','chart-line-up']),
('bank','СБП, любой банк','«Почему Libre.zone»',['landmark','building-bank','building-library','bank']),
('idoff','Без документов','«Почему Libre.zone»',['scan-face','id-off','identification','identification-card']),
('shield','Безопасность','«Почему Libre.zone»',['shield-check','shield-check','shield-check','shield-check']),
('percent','Без скрытых комиссий','«Почему Libre.zone»',['percent','percentage','receipt-percent','percent']),
('gift','Реферальная программа','профиль',['gift','gift','gift','gift']),
]
def inner(p):
    s=open(p).read()
    s=re.sub(r'<svg[^>]*>','',s,1).replace('</svg>','')
    s=re.sub(r'<path stroke="none"[^>]*/>','',s)
    s=re.sub(r'<!--.*?-->','',s,flags=re.S)
    return re.sub(r'\s+',' ',s).strip()
out={}
for k,l,u,n in W:
    d={'cur':IC[k],'label':l,'use':u,
     'lu':inner(R+f'lucide-static/icons/{n[0]}.svg'),
     'tb':inner(R+f'@tabler/icons/icons/outline/{n[1]}.svg'),
     'hr':inner(R+f'heroicons/24/outline/{n[2]}.svg'),
     'hs':inner(R+f'heroicons/24/solid/{n[2]}.svg')}
    for w in ['thin','light','regular','bold','duotone','fill']:
        d['ph_'+w]=inner(R+f'@phosphor-icons/core/assets/{w}/{n[3]}'+('' if w=='regular' else '-'+w)+'.svg')
    out[k]=d
json.dump(out,open(S+'icons_data.json','w'),ensure_ascii=False)
print(len(out), sum(len(json.dumps(v)) for v in out.values())//1024,'KB')
