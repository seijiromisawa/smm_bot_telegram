# Проект SMM-эксперт для Telegram

## Цель проекта

Разработка SMM-эксперта в формате чат-бота для Telegram, способного автоматически генерировать качественный контент о путешествиях. Бот создаёт как текстовые посты (советы, маршруты, описания интересных мест), так и изображения, соответствующие тематике публикаций, и публикует их по заданному расписанию в Telegram-группе.

## Общая информация

Проект предусматривает создание Telegram-бота с интеграцией двух ключевых API:
- **OpenAI API** (ChatGPT для генерации текстов и DALL-E), обеспечивающий творческую генерацию контента.
- **Telegram Bot API**, позволяющий обрабатывать входящие сообщения от пользователей.
- **Make** для организации публикаций по расписанию.

Бот также предлагает рекомендации по контенту и автоматически публикует созданные посты.

## Область применения

### Проблематика

Владельцы Telegram-групп и блогеры о путешествиях сталкиваются с проблемой регулярной публикации качественного контента. Ручное создание постов требует значительных временных затрат и творческих усилий, что может негативно сказываться на активности аудитории.

### Целевая аудитория

Основными пользователями системы являются администраторы Telegram-групп о путешествиях, стремящиеся автоматизировать процесс генерации и публикации контента.

## Функциональные возможности

### Основные функции бота

- **Генерация контента:**
  - Создание текстовых постов с советами, маршрутами и описаниями интересных мест.
  - Автоматическая генерация описаний для постов.
  - Создание тематических изображений, соответствующих сгенерированным текстам.

- **Автоматизация публикаций:**
  - Планирование публикаций с возможностью настройки времени и частоты размещения постов.
  - Автоматическая публикация сгенерированного контента в Telegram-группе.

### Описание проекта и коммерческое предложение

[Коммерческое предложение](./Documents/business-proposal.md)

### Запуск приложения
Требования:
  - Python 3.9.6
  - аккаунт в OpenApi
  - аккаунт в FastCron
  - фккаунт в телеграм

Установите зависимости из файла `requirements.txt`
```bash
pip install -r requirements.txt
```

Создайте `.env` файл и запишите в него переменные среды:
```env
TELEGRAM_TOKEN="your telegram token"
OPENAI_API_KEY="your api-token"
FAST_CRON_KEY="your fast cron token"
```

Запуск приложения
```bash
python bot.py
```
