import sys,json,os;sys.path.insert(0,'/tmp/claude-0/-home-claude/5e080788-a862-58d0-bbc6-f045f9ba6517/scratchpad/ref3')
from run_exp import *
def nomodal(pg):
    pg.evaluate("(()=>{const b=document.querySelector('#layer .modal button');if(b)b.click()})()");pg.wait_for_timeout(500)
def fill_addr(pg):
    pg.evaluate("(()=>{const i=document.querySelector('.card .inp input');i.value='TqRsDBoPDju5bT9fVyMjsF7VfVRbqMKuDb';i.dispatchEvent(new Event('input',{bubbles:true}))})()");pg.wait_for_timeout(300)
def login(pg,step):
    demo(pg,'auth:ask');act(pg,'[data-act="home-continue"]',800)
    if step>=2: act(pg,'[data-act="lphone"]',500);act(pg,'[data-act="d:l:phone"]',300)
    if step>=3: act(pg,'[data-act="lcode"]',500);act(pg,'[data-act="d:l:codeok"]',300)
    if step>=4: act(pg,'[data-act="lcheck"]',700)
def U(pg): demo(pg,'auth:in')
def newfilled(pg):
    U(pg);demo(pg,'go:new');pg.evaluate("document.querySelector('[data-act=\"sheet:bank\"]').click()");pg.wait_for_timeout(600);act(pg,'[data-act="bank:tbank"]',500);fill_addr(pg)
def order(st):
    def f(pg):U(pg);demo(pg,'go:order');act(pg,'[data-act="d:st:%s"]'%st,700)
    return f
STATES=[
 ('01','Главная',lambda pg:(U(pg),demo(pg,'go:home')),'full'),
 ('02','Главная · вне часов',lambda pg:(U(pg),demo(pg,'mode:off'),demo(pg,'go:home')),'full'),
 ('03','Главная · криптовалюта',lambda pg:(U(pg),demo(pg,'go:home'),act(pg,'[data-act="sheet:cur"]',800)),'vp'),
 ('04','Главная · уведомления',lambda pg:(U(pg),demo(pg,'go:home'),act(pg,'[data-act="notes"]',800)),'vp'),
 ('05','Вход · способ',lambda pg:login(pg,1),'vp'),
 ('06','Вход · номер',lambda pg:login(pg,2),'vp'),
 ('07','Вход · код',lambda pg:login(pg,3),'vp'),
 ('08','Вход · регистрация',lambda pg:login(pg,4),'vp'),
 ('09','Новый обмен · реквизиты',lambda pg:(U(pg),demo(pg,'go:new')),'vp'),
 ('10','Новый обмен · банк',lambda pg:(U(pg),demo(pg,'go:new'),pg.evaluate("document.querySelector('[data-act=\"sheet:bank\"]').click()"),pg.wait_for_timeout(700)),'vp'),
 ('11','Новый обмен · заполнено',newfilled,'vp'),
 ('12','Новый обмен · проверка',lambda pg:(newfilled(pg),act(pg,'[data-act="step2"]',600)),'vp'),
 ('13','Новый обмен · согласие',lambda pg:(newfilled(pg),act(pg,'[data-act="step2"]',600),act(pg,'[data-act="agree"]',300)),'vp'),
 ('14','Обмен · создан',order('created'),'full'),
 ('15','Обмен · оплата, Сбер',lambda pg:(demo(pg,'sc:buy-sber',900)),'full'),
 ('16','Обмен · оплата, Т-Банк',lambda pg:(demo(pg,'sc:buy-tbank',900)),'full'),
 ('17','Обмен · мало времени, чек',lambda pg:(demo(pg,'sc:late',900)),'full'),
 ('18','Обмен · продажа, отправка',lambda pg:(demo(pg,'sc:sell-pay',900)),'full'),
 ('19','Обмен · продажа, мало времени',order('soon'),'full'),
 ('20','Обмен · проверка AML',order('verify'),'full'),
 ('21','Обмен · ожидание фиата',lambda pg:(demo(pg,'sc:sell-fiat',900)),'full'),
 ('22','Обмен · завершён',order('done'),'full'),
 ('23','Обмен · пригласи друга',lambda pg:(U(pg),demo(pg,'go:order'),act(pg,'[data-act="d:st:done"]',3300)),'vp'),
 ('24','Обмен · время вышло',order('timeout'),'vp'),
 ('25','Обмен · время вышло, закрыто',lambda pg:(order('timeout')(pg),nomodal(pg)),'full'),
 ('26','Обмен · отменён',lambda pg:(order('cancelled')(pg),nomodal(pg)),'full'),
 ('27','Обмен · деньги не пришли',lambda pg:(U(pg),demo(pg,'go:order'),act(pg,'[data-act="d:err:norecv"]',700),nomodal(pg)),'full'),
 ('28','Мои обмены',lambda pg:(U(pg),demo(pg,'go:orders')),'full'),
 ('29','Мои обмены · активные',lambda pg:(demo(pg,'sc:sell-fiat',900),demo(pg,'go:orders'),act(pg,'[data-act="filter:active"]',400)),'vp'),
 ('30','Мои обмены · ошибки',lambda pg:(demo(pg,'sc:fail',900)),'full'),
 ('31','Профиль',lambda pg:(U(pg),demo(pg,'go:profile')),'full'),
 ('32','Профиль · редактирование',lambda pg:(U(pg),demo(pg,'go:profile'),act(pg,'[data-act="edit"]',500)),'full'),
 ('33','Профиль · выход',lambda pg:(U(pg),demo(pg,'go:profile'),act(pg,'[data-act="logoutq"]',700)),'vp'),
 ('34','Правила и политика',lambda pg:(U(pg),demo(pg,'go:profile'),act(pg,'[data-act="docs"]',600)),'vp'),
 ('35','Правила сервиса',lambda pg:(U(pg),demo(pg,'go:profile'),act(pg,'[data-act="docs"]',600),act(pg,'[data-act^="doc:"]',600)),'full'),
]
def count(n):return 1+sum(count(c) for c in n.get('ch',[]))
if __name__=='__main__':
    only=sys.argv[1:]
    os.makedirs(S+'ref3/st',exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch()
        for sid,name,fn,mode in STATES:
            if only and sid not in only:continue
            pg=b.new_page(viewport={'width':1300,'height':1000});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto('file://'+S+'t_v3.html');pg.wait_for_timeout(500)
            demo(pg,'speed:1');demo(pg,'hints:on');demo(pg,'theme:light')
            pg.add_style_tag(content='.demo{display:none!important}')
            fn(pg);pg.wait_for_timeout(300)
            if mode=='full':pg.evaluate(EXP);pg.wait_for_timeout(200)
            L=export(pg);pg.locator('.phone').first.screenshot(path=S+'ref3/st/%s_L.png'%sid)
            pg.evaluate("document.documentElement.setAttribute('data-theme','dark');document.getElementById('phone').setAttribute('data-mode','dark')");pg.wait_for_timeout(300)
            if mode=='full':pg.evaluate(EXP);pg.wait_for_timeout(200)
            D=export(pg);pg.locator('.phone').first.screenshot(path=S+'ref3/st/%s_D.png'%sid)
            json.dump({'id':sid,'name':name,'mode':mode,'L':L,'D':D},open(S+'ref3/st/%s.json'%sid,'w'),ensure_ascii=False)
            print(sid,name,count(L),count(D),L['h'],errs[:1])
            pg.close()
