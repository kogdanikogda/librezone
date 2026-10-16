# Макеты Figma

Файл: https://www.figma.com/design/jqZVFffwL1sr7I2bqepGIP/  
Страница: **Libre.zone v3 · Mobile** (id `27507:27471`).  
Оригинальные экраны (Showcase) не тронуты.

## Токены
Коллекция переменных **Libre v3**, режимы Light и Dark: цвета (`color/page`, `surface`, `field`, `text`, `text2`, `text3`, `line`, `brand`, `brand-soft`, `brand-dis`, `on-brand`, `grad-1..3`, `btn-dis`, `ok/warn/err` и их фоны, `badge`, `scrim`, `on-grad*`), радиусы (`radius/card`, `field`, `pill`), отступы (`space/page`, `space/gap`).  
Текстовые стили (Manrope): Display/H1, Heading/H2, Heading/H3, Body/Strong, Body/Regular, Body/Small, Caption, Number/Large, Button. Эффект: Shadow/Card.

## Компоненты (всё на auto layout)
| Компонент | Свойства |
|---|---|
| `icon/*` (13 штук, Mingcute Line) | — |
| Header | Badge (boolean), Count (text) |
| Tabbar | Active = home / orders / profile |
| Button | Style = Primary / Outline / Disabled; Label |
| Status tag | Tone = ok / err / info / neu |
| Order card | Tone = ok / err / neu; Id, Route, Date, Repeat |
| Notification row | Tone = info / ok / err / neu; Title, Description, Time, Unread, Chevron |
| Field | State = View / Edit / Locked; Label, Value |
| Tile | Title, Text |

## Экраны (390 × 844)
Светлая тема: Главная, Мои обмены, Уведомления, Профиль, Профиль · редактирование.  
Тёмная тема (те же экраны, режим Dark переменных): Главная, Мои обмены, Уведомления, Профиль.

## Что ещё не перенесено
Новый обмен, экран обмена со статусами, вход, документы, планшет / Mini App, логотип-спираль в шапке (в макете пока текстовый логотип).
