/* ---------- order ---------- */
function copyF(label,val){return '<div class="fld"><span class="lbl2">'+label+'</span><div class="inp ro"><input readonly value="'+esc(val)+'" aria-label="'+esc(label)+'"><button class="copy-i" data-act="copy:'+esc(val)+'" aria-label="Скопировать">'+ic('copy',20)+'</button></div></div>'}
function notifyRow(){return '<label class="notify">'+ic('send',24,'#2AABEE')+'<span><b>Уведомления в Telegram</b>Сообщим, когда статус изменится</span><input type="checkbox" class="sw" data-act="notify" '+(S.notify?'checked':'')+' aria-label="Уведомления в Telegram"></label>'}
function waitBlock(t){return '<div class="wait"><span class="spin" aria-hidden="true"></span><span class="purple">'+(t||'Ожидание…')+'</span><span>Закрыть экран можно, мы продолжим обмен</span></div>'+notifyRow()}
function orderRing(labels,cur){var T=labels.length,n=Math.min(cur,T),done=cur>T,c=2*Math.PI*20,nm=labels[n-1],nx=done?'Обмен завершён':'Дальше: '+labels[n];
 return '<div class="stepring in'+(done?' done':'')+'" role="group" aria-label="Этап '+n+' из '+T+'"><div class="ring"><svg width="46" height="46" viewBox="0 0 46 46" aria-hidden="true"><circle cx="23" cy="23" r="20" fill="none" stroke="var(--line)" stroke-width="4"/><circle class="rp" cx="23" cy="23" r="20" fill="none" stroke="'+(done?'var(--ok-ic)':'var(--brand)')+'" stroke-width="4" stroke-linecap="round" stroke-dasharray="'+(c*n/T).toFixed(1)+' '+c.toFixed(1)+'" transform="rotate(-90 23 23)"/></svg><b>'+n+'/'+T+'</b></div><div class="stt"><b>'+nm+'</b><span>'+nx+'</span></div></div>'}
function stepper(labels,cur){return '<div class="stepper" role="list" aria-label="Этапы заявки">'+labels.map(function(l,i){var n=i+1,dn=n<cur,nw=n===cur;return '<div class="stp" role="listitem"><div class="trk"><i class="ln '+(i>0?(n<=cur?'on':''):'off')+'"></i><b class="bul '+(dn?'done':nw?'now':'')+'">'+(dn?ic('checkb',12):n)+'</b><i class="ln '+(i<labels.length-1?(n<cur?'on':''):'off')+'"></i></div><span class="'+(nw?'now':'')+'">'+l+'</span></div>'}).join('')+'</div>'}
function timerHTML(o){return '<div class="timer'+(o.rem<=120000?' warn':'')+'" id="timer"><div class="row">'+ic('clock',16)+'<span>Осталось на '+(o.dir==='buy'?'оплату':'отправку')+'</span><strong id="tval">'+mmss(o.rem)+'</strong></div><div class="bar"><i id="tbar" style="width:'+Math.max(0,o.rem/6000)+'%"></i></div></div>'}
function orderHTML(){
 var o=getOrder(S.openId),buy=o.dir==='buy',gc=CUR[o.giveCode],tc=CUR[o.getCode],cr=buy?tc:gc;
 var h='<h2 class="page">Детали обмена</h2><div class="card"><div class="ohead"><b>'+o.id+'</b><button class="copy-i oid" data-act="copy:'+o.id+'" aria-label="Скопировать номер">'+ic('copy',16)+'</button><span class="sp"></span>'+tag(o)+'</div>';
 h+='<div class="sumline"><div class="num">'+amtFmt(o.giveCode,o.give)+' '+short(o.giveCode)+ic('arrow',16)+amtFmt(o.getCode,o.get)+' '+short(o.getCode)+'</div><span>'+rateStr(cr.code).replace(' ₽','\u00a0₽')+'\u00a0(с\u00a0учётом комиссии)</span></div>';
 var fl=FLOW[o.dir],ix=fl.indexOf(o.status);
 if(ix>=0)h+=orderRing(LAB[o.dir],o.status==='done'?fl.length+1:ix+1);
 if(buy&&(o.status==='created'||o.status==='pay'||o.status==='check'||o.status==='crypto'))h+=copyF('Адрес для получения '+cr.coin,o.addr);
 if(o.status==='created'){h+=waitBlock('Создаём заявку…')+'<button class="btn outline" data-act="cancel">Отменить обмен</button>'}
 else if(o.status==='pay'){
  h+=timerHTML(o);
  if(buy){
   var b=bank(o.bank);
   h+='<div style="font-size:14px;line-height:20px">Выполните перевод с банка <b style="color:var(--brand)">'+esc(b.n)+'</b> по реквизитам ниже:</div>'+copyF('Номер телефона','+7 999 999-99-99')+copyF('Банк','Сбер')+copyF('ФИО получателя','Красноперекопский Владимир Олегович')+copyF('Сумма',nf(o.give,0));
   if(!o.nameOk){h+='<div class="warnbox">'+ic('warn',16)+'<span>Не совершайте перевод, если имя получателя не соответствует указанному выше.</span></div><div class="ask"><b>Имя получателя соответствует?</b><button class="btn primary" data-act="name:yes">Да</button><button class="btn outline" data-act="name:no">Нет</button></div>'}
   else if(b.link){h+='<div class="fld"><span class="lbl2">Приложите ссылку на чек согласно <a href="#" data-act="instr" style="color:var(--brand)">инструкции</a></span><div class="inp"><input id="rlink" data-bind="link" placeholder="https://tbank.ru/…" autocomplete="off" value="'+esc(o.link||'')+'"></div></div><button class="btn primary" id="sendr" data-act="sent" disabled>Отправить</button>'}
   else{h+='<div class="fld"><span class="lbl2">Отправьте чек о переводе по <a href="#" data-act="instr" style="color:var(--brand)">инструкции</a> на нашу почту</span><div class="inp ro"><input readonly value="contact@libre.zone"><button class="copy-i" data-act="copy:contact@libre.zone" aria-label="Скопировать">'+ic('copy',20)+'</button></div></div><button class="btn primary" data-act="sent">Чек отправлен</button>'}
  }else{
   h+='<div class="warnbox">'+ic('warn',16)+'<span>Отправьте '+esc(gc.coin)+' в сети '+esc(gc.net)+' на адрес ниже. Другая сеть приведёт к потере средств.</span></div>'+copyF('Адрес кошелька',gc.dep)+copyF('Сумма, '+gc.coin,nf(o.give,2))+'<button class="btn primary" data-act="sent">Я отправил(а)</button>';
  }
  h+='<button class="btn outline" data-act="cancel">Отменить обмен</button>';
 }else if(o.status==='check'){h+=waitBlock('Проверяем чек…')}
 else if(o.status==='aml'){h+=waitBlock('Проверка AML…')}
 else if(o.status==='crypto'){h+='<div class="okbox">'+ic('checkc',16)+'<span>Вы перевели '+nf(o.give,0)+' RUB<br>на карту 1234 5678 3482 4828</span></div>'+waitBlock('Ожидание криптовалюты…')}
 else if(o.status==='fiat'){
  h+='<div class="okbox">'+ic('checkc',16)+'<span>Криптовалюта получена. Мы отправили '+nf(o.get,0)+' RUB на реквизиты '+esc(o.addr)+' ('+esc(bank(o.bank).n)+').</span></div>'+
   '<div class="timer'+(o.frem<=300000?' warn':'')+'" id="ftimer"><div class="row">'+ic('clock',16)+'<span>Рубли обычно приходят в течение 30 минут</span><strong id="fval">'+mmss(o.frem)+'</strong></div></div>'+
   '<div class="ask"><b>Получены ли средства?</b><button class="btn primary" data-act="got:yes">Да, деньги пришли</button><button class="btn outline" data-act="got:no">Нет, не пришли</button></div>'+notifyRow();
 }else if(o.status==='done'){
  var dt=o.date.replace(', ',' | ');
  h+='<div class="history">'+(buy?'<div class="histi"><span>Вы перевели '+nf(o.give,0)+' RUB на +7 999 999-99-99</span><small>'+dt+'</small></div><div class="histi"><span>Вам перевели '+amtFmt(o.getCode,o.get)+' '+esc(cr.net)+' на '+esc(o.addr)+'</span><small>'+dt+'</small></div>':'<div class="histi"><span>Вы перевели '+nf(o.give,2)+' '+esc(gc.coin)+' на '+esc(gc.dep)+'</span><small>'+dt+'</small></div><div class="histi"><span>Вам перевели '+nf(o.get,0)+' RUB на '+esc(o.addr)+'</span><small>'+dt+'</small></div>')+'</div><div class="bigdone">'+ic('checkc',36,'var(--ok-ic)')+'<span>Обмен завершён</span></div><button class="btn primary" data-act="repeat:'+o.id+'">'+ic('redo',16)+'Повторить обмен</button><button class="btn outline" data-act="back">Мои обмены</button>';
 }else if(o.status==='cancelled'){
  h+='<div class="warnbox">'+ic('warn',16)+'<span>Обмен отменён по вашему запросу</span></div><button class="btn primary" data-act="repeat:'+o.id+'">'+ic('redo',16)+'Повторить обмен</button><button class="btn outline" data-act="back">Мои обмены</button>';
 }else{
  var msg={nosend:'Вы не отправили средства',norecv:'Вы сообщили, что средства не получены',name:'Вы сообщили, что имя получателя не соответствует',receipt:'Чек не прошёл проверку'}[o.err];
  h+='<div class="warnbox">'+ic('warn',16)+'<span>'+msg+'</span></div>'+(o.err!=='nosend'?'<button class="btn primary" data-act="support:'+o.id+'">'+ic('send',16)+'Написать в поддержку</button>':'<button class="btn primary" data-act="repeat:'+o.id+'">'+ic('redo',16)+'Повторить обмен</button>')+'<button class="btn outline" data-act="back">Мои обмены</button>';
 }
 h+=dchips('Демо: состояние заявки',[['Создан','st:created'],['Ожидание платежа','st:pay'],['Мало времени','st:soon'],['Проверка','st:verify'],['Ожидание '+(buy?'крипты':'фиата'),'st:wait'],['Завершён','st:done'],['Время вышло','st:timeout'],['Отменён','st:cancelled']].concat(buy?[['Чек не прошёл','err:receipt'],['Имя не совпало','err:name']]:[]).concat([['Деньги не пришли','err:norecv']]));
 if(o.status==='pay'&&buy&&o.nameOk&&bank(o.bank).link)h+=dchips('Демо: ссылка на чек',[['Верная ссылка','link:ok'],['Неверная ссылка','link:bad']]);
 return nav(false)+'<div class="content" id="scroller">'+h+'</div></div>';
}
var FILT=[['all','Все'],['active','Активные'],['done','Завершённые'],['failed','Ошибки']];
function inFilter(o){var f=S.filter;if(f==='all')return true;if(f==='done')return o.status==='done';if(f==='failed')return o.status==='error'||o.status==='cancelled';return o.status!=='done'&&o.status!=='error'&&o.status!=='cancelled'}
function ordersHTML(){
 var list=S.orders.filter(inFilter);
 var cards=list.length?list.map(function(o){var fin=o.status==='done'||o.status==='error'||o.status==='cancelled';return '<div class="ocard" role="button" tabindex="0" data-act="open:'+o.id+'"><div class="r"><b>'+o.id+'</b>'+tag(o)+'</div><div class="l"><span class="c">'+esc(CUR[o.giveCode].name)+'</span><span class="num">'+amtFmt(o.giveCode,o.give)+'</span>'+ic('arrow',16)+'<span class="c">'+esc(CUR[o.getCode].name)+'</span><span class="num">'+amtFmt(o.getCode,o.get)+'</span></div><div class="d"><span>'+o.date+'</span>'+(fin?'<button class="rep" data-act="repeat:'+o.id+'">'+ic('redo',16)+'Повторить</button>':'')+'</div></div>'}).join(''):'<div class="none">В этой категории обменов нет</div>';
 return nav(false)+'<div class="content" id="scroller"><h2 class="page">Мои обмены</h2><div class="filters" role="group" aria-label="Фильтр">'+FILT.map(function(f){return '<button class="fchip" data-act="filter:'+f[0]+'" aria-pressed="'+(S.filter===f[0])+'">'+f[1]+'</button>'}).join('')+'</div><div class="olist">'+cards+'</div>'+dchips('Демо',[['Добавить покупку','o:buy'],['Добавить продажу','o:sell']])+'</div>';
}
function profileHTML(){
 var u=S.profile,ro=!S.edit;
 function f(id,l,v,lock){var r=ro||lock;var ed=!ro&&!lock;return '<div class="fld'+(lock?' locked':'')+'"><label class="lbl2" for="'+id+'">'+l+'</label><div class="inp'+(r?' ro':'')+(ed?' ed':'')+'"><input id="'+id+'" data-bind="'+id+'" value="'+esc(v)+'" '+(r?'readonly disabled':'')+(lock?' aria-describedby="'+id+'h"':'')+'>'+(lock&&S.edit?'<span class="lk" title="Изменить нельзя">'+ic('lock',20)+'</span>':'')+(ed?'<span class="pen">'+ic('edit',20)+'</span>':'')+'</div>'+(lock&&S.edit?'<div class="hint" id="'+id+'h">'+lock+'</div>':'')+'</div>'}
 var act=S.edit?'<button class="btn primary" data-act="save">Сохранить изменения</button>':(S.saved?'<button class="btn primary" data-act="edit">'+ic('check',16)+'Сохранено</button>':'<button class="btn outline" data-act="edit">Редактировать профиль</button>');
 var h='<h2 class="page">Профиль</h2><section class="card pf'+(S.edit?' editing':'')+'">'+f('pfio','Ф.И.О.',u.fio)+f('pemail','Email',u.email)+f('pphone','Телефон',u.phone,'Номер телефона привязан к аккаунту, изменить его нельзя')+act+(S.edit?dchips('Демо-данные',[['Другие данные','prof:other']]):'')+'</section>'+
  '<section class="card"><h3 style="margin:0;font-family:var(--fd);font-size:20px;line-height:28px;font-weight:700;letter-spacing:-.015em">Реферальная программа</h3><div class="refbox"><span>Зарабатывайте скидки, делясь Libre.zone с друзьями.</span><ol class="reflist"><li>Отправьте ссылку друзьям.</li><li>Друг регистрируется по вашей ссылке и получает купон $2 на обмен от 20 000 ₽.</li><li>Друг завершает первый обмен.</li><li>Вы получаете скидку 10% на комиссию следующего обмена за каждого приглашённого друга.</li></ol></div>'+
  copyF('Моя партнёрская ссылка','https://dev.libre.zone/partner/cd76gcfrk')+'<button class="btn soft" data-act="share">'+ic('send',16)+'Поделиться в Telegram</button><div><div class="stat"><span>Приглашённых друзей</span><b>0</b></div><div class="stat"><span>Обменов со скидкой 10%</span><b>0</b></div></div></section>';
 var th=$('#phone').getAttribute('data-mode')==='dark'?'dark':'light';
 function seg2(act,items,cur){return '<span class="seg2" role="group">'+items.map(function(x){return '<button data-act="'+act+':'+x[0]+'" aria-pressed="'+(cur===x[0])+'"'+(x[2]?' aria-label="'+x[2]+'"':'')+'>'+x[1]+'</button>'}).join('')+'</span>'}
 h+='<h3 class="grp">Помощь</h3><section class="card rows">'+
   '<button class="row tgrow" data-act="support:">'+ic('send',20,'#2AABEE')+'<span class="g">Чат поддержки в Telegram<small>Отвечаем 10:00–18:30 МСК</small></span>'+ic('chevl',20).replace('class="ic"','class="ic flip"')+'</button>'+
   '<div class="row">'+ic('mail',20)+'<span class="g">support@libre.zone<small>Для чеков и документов</small></span><button class="mini-copy" data-act="copy:support@libre.zone" aria-label="Скопировать email">'+ic('copy',20)+'</button></div></section>'+
  '<h3 class="grp">Настройки</h3><section class="card rows">'+
   '<label class="row">'+ic('bell',20)+'<span class="g">Уведомления в Telegram<small>О смене статуса обмена</small></span><input type="checkbox" class="sw" id="pnotif" checked></label>'+
   '<div class="row">'+ic('globe',20)+'<span class="g">Язык</span>'+seg2('lang',[['ru','RU'],['en','EN']],'ru')+'</div>'+
   '<div class="row">'+ic('sun',20)+'<span class="g">Тема</span>'+seg2('ptheme',[['light',ic('sun',16),'Светлая'],['dark',ic('moon',16),'Тёмная']],th)+'</div></section>'+
  '<section class="card rows"><button class="row" data-act="docs">'+ic('doc',20)+'<span class="g">Правила и политика</span>'+ic('chevl',20).replace('class="ic"','class="ic flip"')+'</button></section>'+
  '<button class="btn outline danger-t" data-act="logoutq">'+ic('logout',16)+'Выйти из аккаунта</button>'+
  '<div class="foot" style="padding-top:8px">Libre.zone · Вход защищён Google reCAPTCHA</div>';
 return nav(false)+'<div class="content" id="scroller">'+h+'</div>';
}
function menuHTML(){
 return '<div class="menu" role="dialog" aria-modal="true" aria-label="Меню"><header class="nav"><div class="logo">'+logoMark()+'<span>Libre<b>.zone</b></span></div><button class="burger" data-act="menu" aria-label="Закрыть меню">'+ic('close',24)+'</button></header><ul><li><button data-act="go:new">Новый обмен</button></li><li><button data-act="go:orders">Мои обмены</button></li><li><button data-act="go:profile">Мой профиль</button></li><li><button data-act="logout">'+ic('logout',24)+'Выйти</button></li></ul><div class="mfoot"><div>'+ic('mail',20)+'support@libre.zone</div><div>'+ic('clock',20)+'Техподдержка 10:00–18:30 GMT+3</div><div>'+ic('shield',20)+'Используется Google reCAPTCHA</div><button class="tg" data-act="support:">'+ic('send',20,'#2AABEE')+'Чат поддержки в Telegram</button></div></div>';
}

