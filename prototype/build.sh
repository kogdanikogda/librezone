#!/bin/sh
# Сборка прототипа: src/part1.html (разметка и CSS) + src/js/*.js (по порядку номеров)
cd "$(dirname "$0")" && cat src/part1.html src/js/*.js | sed "s/__BUILD__/$(TZ=Europe/Moscow date '+%d.%m %H:%M') МСК/" > libre-zone-v3.html && node -e "
const h=require('fs').readFileSync('libre-zone-v3.html','utf8');let ok=1;for(const x of h.matchAll(/<script>([\s\S]*?)<\/script>/g)){try{new Function(x[1])}catch(e){ok=0;console.log('ОШИБКА',e.message)}}console.log(ok?'сборка ок':'сборка с ошибкой')"
