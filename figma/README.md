# Макеты Figma — Libre.Zone 2.0

Файл: https://www.figma.com/design/8AzhfYFeMH3XJBfWboYR39/Libre.Zone-2.0  
Файл пересобран с нуля: всё на auto layout, компоненты со свойствами, только токены (без сырых цветов).

## Страницы
| Страница | Что внутри |
|---|---|
| Cover | Обложка |
| Foundations | Образцы цветов (Light/Dark), типографика, отступы, радиусы, тени |
| Icons | 42 иконки Mingcute Line как компоненты `Icon/<name>` |
| Components | 17 наборов компонентов |
| Screens | 8 экранов 390×844 × 2 темы, прототип со ссылками между экранами |

## Токены (переменные)
- **Primitives** → **Color** (Light / Dark, алиасы на примитивы) → **Dimensions** (space, radius, size).
- Текстовые стили Manrope: Display/H1, Heading/H2, H3, Logo, Number/Large, Body/Strong, Regular, Small, Caption, Button.
- Эффекты: Shadow/Card, Soft, Nav, Sheet, Brand.

## Компоненты
Logo (Wordmark) · Icon button (Style, Icon, Badge, Count) · Button (Style × Size × State; Label, Icon, Show icon) · Status tag (Tone) · Chip (Selected) · Tab item / Tabbar · Header · Field (View/Edit/Locked/Error) · Order card (Tone) · Notification row (Tone; Title, Description, Time, Unread) · Option row · Timer · Tile · Amount row · Sheet (Content — instance swap) + Sheet content · Modal (Tone).

## Экраны
Главная, Новый обмен, Оплата, Мои обмены, Уведомления (шторка), Профиль, Вход (шторка), Выйти? (модальное окно). Светлая и тёмная тема получаются сменой режима коллекции Color. Два flow: Light и Dark, стартуют с «Главная».

Старый файл `jqZVFffwL1sr7I2bqepGIP` больше не используется.
