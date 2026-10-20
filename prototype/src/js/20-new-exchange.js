/* ---------- new exchange ---------- */
function requisiteState(){var v=S.addr.trim(),dg=v.replace(/\D/g,''),tb=S.bank&&bank(S.bank).link;
 var okv=tb?(dg.length===16||dg.length===11):dg.length===11;
 return {ok:okv,bad:v.length>0&&((dg.length>=11&&!okv)||/[^\d+\s-]/.test(v))}}
function addrBad(){return S.dir==='buy'?(S.addr.length>0&&!CUR[S.coin].re.test(S.addr.trim())):requisiteState().bad}
function addrOk(){return S.dir==='buy'?CUR[S.coin].re.test(S.addr.trim()):requisiteState().ok}
function readyStep1(){return !!S.bank&&addrOk()}
function addrHintText(){if(addrBad())return S.dir==='buy'?'Неверный адрес':'Номер указан неверно';return S.dir==='buy'?'Принимаем адреса только в сети '+CUR[S.coin].net:'Только российские номера и карты'}
function noteHTML(){
 var b=S.bank?bank(S.bank):null,t;
 if(S.dir==='buy'){
  if(!b)t='Выберите банк, с которого будете платить. Для большинства банков потребуется веб-версия, чтобы подтвердить перевод.';
  else if(b.link)t='Для Т-Банка достаточно приложить ссылку на чек из приложения после перевода.';
  else t='Потребуется веб-версия выбранного банка для подтверждения транзакции. <a href="#" data-act="why">Почему?</a>';
 }else t='Убедитесь, что реквизиты верны. Сервис не несёт ответственности за потерю средств из-за неверно указанных данных.';
 return '<div class="notebox">'+ic('info',16)+'<span>'+t+'</span></div>'}
/* индикатор шага: кольцо с номером и название шага */
function stepRing(st){var n=st+1,c=2*Math.PI*20,nm=st===1?'Реквизиты':'Проверка',nx=st===1?'Дальше: проверка':'Последний шаг перед оплатой';
 return '<div class="stepring" role="group" aria-label="Шаг '+n+' из 3"><div class="ring"><svg width="46" height="46" viewBox="0 0 46 46" aria-hidden="true"><circle cx="23" cy="23" r="20" fill="none" stroke="var(--line)" stroke-width="4"/><circle cx="23" cy="23" r="20" fill="none" stroke="var(--brand)" stroke-width="4" stroke-linecap="round" stroke-dasharray="'+(c*n/3).toFixed(1)+' '+c.toFixed(1)+'" transform="rotate(-90 23 23)"/></svg><b>'+n+'/3</b></div><div class="stt"><b>'+nm+'</b><span>'+nx+'</span></div></div>'}
function newHTML(){
 var buy=S.dir==='buy',c=CUR[S.coin],b=S.bank?bank(S.bank):null,st=S.step,tb=b&&b.link,body;
 var strip='<div class="sumstrip"><div><span>Отдаёте</span><b class="num">'+sideStr('give')+' '+short(giveC())+'</b></div>'+ic('arrow',16)+'<div><span>Получаете</span><b class="num">'+sideStr('get')+' '+short(getC())+'</b></div><button class="link" data-act="edit-amount">Изменить</button></div>';
 var head='<button class="back" data-act="newback">'+ic('chevl',16)+'Назад</button>'+strip+''+stepRing(st);
 if(st===1){
  var bl=buy?'Банк отправки':'Банк получения';
  var al=buy?'Адрес кошелька в сети '+c.net:(b?(tb?'Номер карты или телефона':'Номер телефона для СБП'):'Номер телефона или карты');
  var ph=buy?'Вставьте адрес':(b?(tb?'Номер телефона или карты':'Номер телефона'):'Сначала выберите банк');
  body='<div class="card"><div class="fld"><span class="lbl2">'+bl+'</span><button class="sel" data-act="sheet:bank" aria-haspopup="dialog">'+(b?bdot(b.id)+'<span class="grow">'+esc(b.n)+'</span>':'<span class="grow ph">Выберите банк</span>')+ic('chevd',20)+'</button></div>'+
   '<div class="fld"><label class="lbl2" for="addr">'+al+'</label><div class="inp'+(addrBad()?' bad':'')+'"><input id="addr" data-bind="addr" '+((!buy&&!b)?'disabled ':'')+'inputmode="'+(buy?'text':'tel')+'" autocomplete="off" spellcheck="false" placeholder="'+ph+'" value="'+esc(S.addr)+'"></div><div class="hint'+(addrBad()?' bad':'')+'" id="ahint">'+addrHintText()+'</div></div>'+
   '<div id="noteslot">'+noteHTML()+'</div></div>'+dchips('Демо-данные',buy?[['Т-Банк','bank:tbank'],['СберБанк','bank:sber'],['Верный адрес','addr:ok'],['Адрес другой сети','addr:net'],['Короткая строка','addr:short']]:[['Т-Банк','bank:tbank'],['СберБанк','bank:sber'],['Телефон СБП','addr:ok'],['Карта Т-Банка','addr:card'],['Неверный номер','addr:bad']]);
 }else{
  var i=CHIPS.indexOf(S.amount),eta=i>=0?ETA[QBARS[i]][0]:'—';
  body='<div class="card"><div><div class="rv"><span>Отдаёте</span><b class="num">'+sideStr('give')+' '+short(giveC())+'</b></div><div class="rv"><span>Получаете</span><b class="num">'+sideStr('get')+' '+short(getC())+'</b></div><div class="rv"><span>Курс</span><b class="num">'+rateStr(S.coin)+'</b></div><div class="rv"><span>Комиссия</span><b>Включена в курс</b></div><div class="rv"><span>Ожидаемое время</span><b>'+eta+'</b></div><div class="rv"><span>'+(buy?'Банк отправки':'Банк получения')+'</span><b>'+(b?esc(b.n):'—')+'</b></div><div class="rv"><span>'+(buy?'Адрес кошелька':'Реквизиты')+'</span><b class="num">'+esc(S.addr.trim())+'</b></div></div></div>'+
   '<label class="check"><input type="checkbox" id="agree" data-act="agree" '+(S.agree?'checked':'')+'><span>Я соглашаюсь с <a href="#" data-act="rules">правилами сервиса</a> и подтверждаю, что реквизиты указаны верно</span></label>'+dchips('Демо-данные',[['Принять правила','agree']]);
 }
 var cta=st===1?'<button class="btn primary" id="next" data-act="step2" disabled>Далее</button>':'<button class="btn primary" id="create" data-act="create" disabled>Обменять валюту</button>';
 return nav(false)+'<div class="content split"><div class="scrollarea" id="scroller">'+head+body+'</div><div class="dock">'+cta+'</div></div>';
}
function readyNew(){return S.step===2&&readyStep1()&&S.agree}

