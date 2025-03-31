# Руководство по развертыванию стоматологического приложения

Это руководство поможет развернуть приложение для стоматологической практики на сервере.

## Предварительные требования

- Docker
- Docker Compose
- Git
- Доступ к API ключу OpenAI
- Доступ к API ключу Airtable

## Клонирование репозитория

```bash
git clone [URL-репозитория]
cd DENT_AGENT
```

## Настройка переменных окружения

1. Скопируйте пример файла окружения:

```bash
cp example.env .env
```

2. Отредактируйте файл `.env`, вставив ваши ключи API и другие настройки:

```
# Airtable API Configuration
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id_here
AIRTABLE_PROCEDURES_TABLE=Procedures
AIRTABLE_CATEGORIES_TABLE=Categories

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# Default language for prompts
DEFAULT_LANGUAGE=ru
```

## Запуск приложения с Docker Compose

1. Запустите приложение:

```bash
docker-compose up -d
```

2. Приложение будет доступно по адресу: `http://[ваш-сервер]:8501`

## Остановка приложения

```bash
docker-compose down
```

## Обновление приложения

1. Получите последние изменения из репозитория:

```bash
git pull
```

2. Перезапустите контейнер с обновленным кодом:

```bash
docker-compose down
docker-compose up -d --build
```

## Логи и отладка

Просмотр логов контейнера:

```bash
docker-compose logs -f
```

## Структура проекта

- `dental_assistant/frontend/app.py` - Основное Streamlit приложение
- `dental_assistant/frontend/report_generator.py` - Генератор отчетов
- `prompts/` - Шаблоны промптов для различных типов процедур
- `procedures/` - Данные о процедурах

## Резервное копирование данных

База данных Airtable хранится в облаке, поэтому нет необходимости в локальном резервном копировании.

## Доступ и безопасность

По умолчанию приложение доступно только на локальном сервере. Для публичного доступа настройте обратный прокси-сервер (например, Nginx) с SSL-сертификатом. 