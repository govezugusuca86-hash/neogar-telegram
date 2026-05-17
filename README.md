# Отложенный постинг Neogar → Telegram

Каждые 2 часа (с 7:00 до 21:00 по Москве) GitHub автоматически публикует один пост в канал @neogar_shop. 20 постов → 2.5 дня. Бесплатно, без сервера.

## Шаг 1. Создай новый репозиторий

1. Зайди на github.com
2. Нажми **+** → **New repository**
3. Название: `neogar-telegram` (или любое)
4. **Private** (приватный — чтобы токен не светился)
5. Нажми Create

## Шаг 2. Загрузи файлы

1. В репозитории нажми **Add file → Upload files**
2. Перетащи ВСЕ файлы и папки из этого ZIP:
   - `.github/workflows/telegram-post.yml`
   - `publish_one.py`
   - `posts/posts.json`
   - `photos/` (все 11 фото)
3. Нажми **Commit changes**

Важно: папка `.github` может не отображаться в проводнике Windows (скрытая). Покажи скрытые файлы или загружай через git.

Проще всего через git:
```bash
git clone https://github.com/govezugusuca86-hash/neogar-telegram.git
# скопируй все файлы из ZIP в эту папку
git add .
git commit -m "initial"
git push
```

## Шаг 3. Добавь секреты

1. В репозитории: **Settings → Secrets and variables → Actions**
2. Нажми **New repository secret**
3. Добавь два секрета:

| Name | Value |
|------|-------|
| `BOT_TOKEN` | `8569719042:AAGkmFPkNJZq9Q8qnJed_W8wYA2snmwlLuM` |
| `CHANNEL_ID` | `-1001622821912` |

## Шаг 4. Включи Actions

1. В репозитории: вкладка **Actions**
2. Если видишь предупреждение — нажми **I understand, enable Actions**
3. Слева найди workflow **Telegram Scheduled Post**
4. Нажми **Run workflow** → **Run workflow** (зелёная кнопка) для теста

## Шаг 5. Проверь

1. После ручного запуска — проверь канал, должен появиться первый пост
2. Дальше посты будут выходить автоматически каждые 2 часа
3. Прогресс сохраняется в `posts/progress.json` — уже опубликованные не повторятся

## Расписание

Посты выходят в: 07:00, 09:00, 11:00, 13:00, 15:00, 17:00, 19:00, 21:00 (МСК)
8 постов в день → все 20 выйдут за 2.5 дня.

Чтобы изменить расписание — отредактируй cron в файле `.github/workflows/telegram-post.yml`

## Кросспостинг в MAX

Если PlanerMax настроен (авторепост TG → MAX) — посты автоматически появятся и в MAX.

## Добавление новых постов

1. Отредактируй `posts/posts.json` — добавь новые записи
2. Положи новые фото в `photos/`
3. Сбрось прогресс: удали `posts/progress.json` или убери ID старых постов из `done`
4. Commit + push — GitHub продолжит по расписанию
