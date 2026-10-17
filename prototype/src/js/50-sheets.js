/* ---------- sheets / modals ---------- */
function sheetWrap(title,body,tall){return '<div class="scrim end" data-act="close"><div class="sheet'+(tall?' tall':'')+'" role="dialog" aria-modal="true" aria-label="'+title+'"><div class="grab"></div><div class="sh"><b>'+title+'</b><button class="xbtn2" data-act="close" aria-label="Закрыть">'+ic('close',20)+'</button></div>'+body+'</div></div>'}
function curSheet(){return sheetWrap('Криптовалюта','<div class="opts">'+COINS.map(function(c){var x=CUR[c];return '<button class="opt" role="option" aria-selected="'+(S.coin===c)+'" data-act="coin:'+c+'">'+cdot(c,32)+'<span class="grow"><b>'+x.coin+'</b><small>сеть '+esc(x.net)+'</small></span><span class="rt num">'+(x.rate>1000?nf(x.rate,0):nf(x.rate,2))+' ₽</span>'+(S.coin===c?ic('check',20).replace('class="ic"','class="ic ck"'):'')+'</button>'}).join('')+'</div>')}
function bankOpt(b){return '<button class="opt" role="option" aria-selected="'+(S.bank===b.id)+'" data-act="bank:'+b.id+'">'+bdot(b.id)+'<span class="grow"><b>'+esc(b.n)+'</b>'+(b.link?'<small>Достаточно ссылки на чек</small>':'')+'</span>'+(S.bank===b.id?ic('check',20).replace('class="ic"','class="ic ck"'):'')+'</button>'}
function bankList(){
 var q=S.q.trim().toLowerCase();
 if(q){var l=BANKS.filter(function(b){return b.n.toLowerCase().indexOf(q)>=0});return l.length?l.map(bankOpt).join(''):'<div class="none">Ничего не найдено</div>'}
 var pop=POPULAR.map(bank),rest=BANKS.filter(function(b){return POPULAR.indexOf(b.id)<0}).sort(function(a,b){return a.n.localeCompare(b.n,'ru')});
 return '<h4>Популярные</h4>'+pop.map(bankOpt).join('')+'<h4>Все банки</h4>'+rest.map(bankOpt).join('')}
function bankSheet(){return sheetWrap(S.dir==='buy'?'Банк отправки':'Банк получения','<div class="inp">'+ic('search',20)+'<input id="bq" data-bind="bq" autocomplete="off" placeholder="Поиск банка" aria-label="Поиск банка" value="'+esc(S.q)+'"></div><div class="opts" id="blist">'+bankList()+'</div>',true)}
function layerHTML(){
 if(S.menu)return menuHTML();
 if(S.login)return loginHTML();
 if(S.sheet==='notes')return notesSheet();
 if(S.sheet==='cur')return curSheet();
 if(S.sheet==='bank')return bankSheet();
 var m=S.modal;
 if(m==='refer')return '<div class="scrim"><div class="modal refer"><button class="xbtn" data-act="close" aria-label="Закрыть">'+ic('close',20)+'</button><div class="logo">'+logoMark()+'<span>Libre<b>.zone</b></span></div><h3>Пригласи друга и получи скидку 10%</h3><p>Друг получит купон на $2 при обмене от 20 000 ₽.</p><button class="btn primary" data-act="to-profile">Подробнее</button></div></div>';
 if(m==='logoutq')return '<div class="scrim"><div class="modal mi"><span class="mic neu">'+ic('logout',30)+'</span><h3>Выйти из аккаунта?</h3><p>Активные обмены продолжатся, статус можно будет проверить после входа.</p><button class="btn danger" data-act="logout">Выйти</button><button class="btn outline" data-act="close">Отмена</button></div></div>';
 if(m==='confirm')return '<div class="scrim"><div class="modal mi"><span class="mic warn">'+ic('warn',30)+'</span><h3>Вы уверены, что хотите отменить обмен?</h3><p>Если вы уже перевели деньги, отменять обмен не нужно.</p><button class="btn primary" data-act="cancel-yes">Да, отменить</button><button class="btn outline" data-act="close">Нет</button></div></div>';
 if(m==='timeout')return '<div class="scrim"><div class="modal mi"><span class="mic err">'+ic('clock',30)+'</span><h3>Время вышло</h3><p>Вы не отправили средства за отведённые 10 минут. Обмен отменён.</p><button class="btn primary" data-act="close">Понятно</button></div></div>';
 if(m==='noname')return '<div class="scrim"><div class="modal mi"><span class="mic err">'+ic('warn',30)+'</span><h3>Не совершайте перевод</h3><p>Имя получателя не соответствует указанному. Напишите в поддержку, мы проверим данные.</p><button class="btn primary" data-act="support:'+(S.openId||'')+'">Написать в поддержку</button><button class="btn outline" data-act="close">Отмена</button></div></div>';
 return '';
}

var ACTIVE=['created','pay','check','aml','crypto','fiat'];
function activeOrders(){return S.orders.filter(function(o){return ACTIVE.indexOf(o.status)>=0})}
function plateHTML(){var a=activeOrders();if(!a.length||S.screen==='order')return '';var o=a[0],s=stat(o),c=CUR[o.dir==='buy'?o.getCode:o.giveCode];
 var t=o.status==='pay'?'<span class="ptm num" id="ptm" data-id="'+o.id+'">'+mmss(o.rem)+'</span>':'<span class="ptm">'+ic('chevl',18).replace('class="ic"','class="ic flip"')+'</span>';
 return '<button class="plate" data-act="open:'+o.id+'" aria-label="Открыть активный обмен '+o.id+'">'+cdot(c.code,30)+'<span class="pt"><b>'+o.id+(a.length>1?' <i>+'+(a.length-1)+'</i>':'')+'</b><span>'+s[0]+'</span></span>'+t+'</button>'}
function tabsHTML(){var n=activeOrders().length,cur=S.screen;
 function t(k,icn,l,b){return '<button class="tab'+(cur===k?' on':'')+'" data-act="tab:'+k+'" aria-current="'+(cur===k?'page':'false')+'">'+ic(icn,22)+'<span>'+l+'</span>'+(b?'<i class="bdg">'+b+'</i>':'')+'</button>'}
 return '<div class="tabzone">'+plateHTML()+'<nav class="tabs" aria-label="Разделы">'+t('home','home','Обмен')+t('orders','list','Мои обмены',n)+t('profile','user','Профиль')+'</nav></div>'}

var DOCS=[
 {id:'rules',icon:'doc',t:'Правила сервиса',d:'Как проходит обмен, сроки, курс, отмена и возврат',
  sum:['Курс фиксируется при создании заявки, комиссия уже в нём','На оплату или отправку — 10 минут, иначе заявка отменяется','Переводите только со своей карты и точную сумму одним платежом','Обмены проводим 10:00–18:30 по Москве (GMT+3)'],
  secs:[
   ['Общие положения',['Libre.zone помогает обменять рубли на криптовалюту и обратно по фиксированным суммам. Создавая заявку, вы соглашаетесь с этими правилами, Политикой конфиденциальности и AML-политикой.','Пользоваться сервисом могут совершеннолетние граждане, которые действуют от своего имени и в своих интересах.']],
   ['Часы работы',['Заявки принимаем и проводим с 10:00 до 18:30 по московскому времени (GMT+3). Заявку, созданную до закрытия, доводим до конца.','Вне рабочих часов создать заявку нельзя. Статус активных обменов всегда виден в разделе «Мои обмены».']],
   ['Суммы, курс и комиссия',['Доступны фиксированные суммы: 50, 100, 1 000, 5 000, 10 000 и 50 000 ₽.','Курс фиксируется в момент создания заявки и не меняется до её завершения. Комиссия сервиса включена в курс, итоговую сумму вы видите до подтверждения. Других списаний нет.','Ожидаемое время обмена зависит от числа встречных заявок и показывается примерно.']],
   ['Покупка криптовалюты',['После создания заявки у вас есть 10 минут, чтобы перевести рубли по указанным реквизитам. Переводите с банка, выбранного в заявке, точную сумму одним платежом.','Перевод должен идти с карты или счёта, открытого на ваше имя. Перед оплатой сверьте имя получателя с указанным в заявке.','После перевода подтвердите оплату: для Т-Банка достаточно ссылки на чек, для остальных банков отправьте чек на contact@libre.zone.','Криптовалюту отправляем на адрес из заявки в выбранной сети. Адрес другой сети приведёт к потере средств, поэтому проверьте его перед подтверждением.']],
   ['Продажа криптовалюты',['После создания заявки у вас есть 10 минут, чтобы отправить криптовалюту на адрес сервиса в указанной сети.','Поступление проходит AML-проверку. Затем отправляем рубли по СБП или на карту, обычно в течение 30 минут.','Когда деньги придут, подтвердите получение в заявке. Если их нет дольше 30 минут, нажмите «Нет» — мы проверим перевод.']],
   ['Отмена и возврат',['Отменить заявку можно, пока вы не перевели средства. Если таймер истёк, заявка отменяется автоматически.','Если вы перевели средства после отмены или с ошибкой, напишите в поддержку с номером заявки. Вернём средства отправителю после проверки.']],
   ['Когда мы можем приостановить обмен',['Платёж пришёл от третьего лица или с другого банка, сумма не совпадает с заявкой, данные получателя не совпадают, проверка AML выявила риск. В этих случаях мы связываемся с вами и запрашиваем пояснения.']],
   ['Поддержка',['Чат в Telegram и почта support@libre.zone работают в те же часы, что и обмены. Укажите номер заявки, чтобы мы ответили быстрее.']]]},
 {id:'privacy',icon:'shield',t:'Политика конфиденциальности',d:'Какие данные мы собираем, зачем и как их защищаем',
  sum:['Собираем только то, что нужно для обмена и проверки','Не продаём и не передаём данные для рекламы','Данные передаются по защищённому соединению','Можно запросить, исправить или удалить свои данные'],
  secs:[
   ['Какие данные собираем',['Ф.И.О., номер телефона, email, аккаунт Telegram, если вы входите через него.','Реквизиты и адреса кошельков из заявок, история обменов.','Технические данные: тип устройства, браузер, IP-адрес, данные о посещении.']],
   ['Зачем',['Чтобы проводить обмены и отправлять уведомления о статусе.','Чтобы проверять операции по требованиям AML и KYC.','Чтобы отвечать в поддержке и улучшать сервис.']],
   ['Кому передаём',['Банкам и платёжным партнёрам — только данные, нужные для конкретной операции.','Государственным органам — только по требованию закона.','Данные не продаём и не передаём для рекламы.']],
   ['Как храним и защищаем',['Данные передаются по защищённому соединению, доступ к ним есть только у сотрудников, которым он нужен для работы.','Храним данные, пока у вас есть аккаунт, и столько, сколько требует закон после его удаления.']],
   ['Cookies и reCAPTCHA',['Используем cookies, чтобы вы оставались в аккаунте и работали настройки. Вход защищён Google reCAPTCHA, к нему применяются политика конфиденциальности и условия Google.']],
   ['Ваши права',['Вы можете запросить копию своих данных, исправить их или удалить аккаунт. Данные, которые мы обязаны хранить по закону, удалим после окончания срока хранения. Напишите на support@libre.zone.']]]},
 {id:'aml',icon:'checkc',t:'AML и KYC политика',d:'Как мы проверяем пользователей и операции',
  sum:['Для обмена достаточно телефона, Ф.И.О. и email — без селфи и документов','Проверяем, что платёж пришёл от владельца аккаунта','Криптоадреса проходят AML-проверку','При риске можем запросить пояснения или отказать в обмене'],
  secs:[
   ['Проверка пользователя (KYC)',['При регистрации указываете Ф.И.О., телефон и email. Селфи и документы для обычных обменов не нужны.','Ф.И.О. должно совпадать с владельцем карты или счёта, с которых вы платите и на которые получаете рубли.']],
   ['Проверка операций (AML)',['Проверяем, что платёж отправлен с вашей карты, в нужной сумме и с банка из заявки.','Входящие и исходящие криптоадреса проверяем по базам рисков. Средства, связанные с мошенничеством, санкциями или даркнетом, не принимаем.']],
   ['Что может задержать обмен',['Платёж от третьего лица, несовпадение имени, высокий риск адреса. Мы приостановим обмен и напишем вам. Обычно хватает короткого пояснения.']],
   ['Запрещено',['Обмен средств, полученных незаконно, обмен в интересах третьих лиц, дробление сумм ради обхода проверок.']]]}];
function docsHTML(){
 var h='<button class="back" data-act="docback">'+ic('chevl',18)+'Назад</button><h2 class="page">Правила и политика</h2>'+
  '<div class="doclist">'+DOCS.map(function(d){return '<button class="dcard" data-act="doc:'+d.id+'"><span class="wi2">'+ic(d.icon,20)+'</span><span class="g"><b>'+d.t+'</b><small>'+d.d+'</small><em>Редакция от 14.10.2026</em></span>'+ic('chevl',18).replace('class="ic"','class="ic flip"')+'</button>'}).join('')+'</div>'+
  '<section class="card rows"><button class="row tgrow" data-act="support:">'+ic('send',20,'#2AABEE')+'<span class="g">Остались вопросы?<small>Напишите в чат поддержки</small></span>'+ic('chevl',18).replace('class="ic"','class="ic flip"')+'</button></section>';
 return nav(false)+'<div class="content" id="scroller">'+h+'</div>'}
function docHTML(){var d=DOCS.filter(function(x){return x.id===S.doc})[0]||DOCS[0];
 var h='<button class="back" data-act="docback">'+ic('chevl',18)+'Назад</button><h2 class="page">'+d.t+'</h2><div class="dmeta">Редакция от 14.10.2026 · '+d.secs.length+' разделов</div>'+
  '<section class="dsum"><b>Коротко</b><ul>'+d.sum.map(function(s){return '<li>'+ic('check',16)+'<span>'+s+'</span></li>'}).join('')+'</ul></section>'+
  '<nav class="dtoc" aria-label="Содержание">'+d.secs.map(function(s,i){return '<button data-act="dsec:'+i+'">'+(i+1)+'. '+s[0]+'</button>'}).join('')+'</nav>'+
  '<article class="dbody">'+d.secs.map(function(s,i){return '<section id="dsec'+i+'"><h3><span class="n">'+(i+1)+'</span><span class="t">'+s[0]+'</span></h3>'+s[1].map(function(p){return '<p>'+p+'</p>'}).join('')+'</section>'}).join('')+'</article>'+
  '<div class="dnext">'+DOCS.filter(function(x){return x.id!==d.id}).map(function(x){return '<button class="dcard sm" data-act="doc:'+x.id+'"><span class="g"><small>Другие документы</small><b>'+x.t+'</b></span>'+ic('chevl',18).replace('class="ic"','class="ic flip"')+'</button>'}).join('')+'</div>';
 return nav(false)+'<div class="content" id="scroller">'+h+'</div>'}

