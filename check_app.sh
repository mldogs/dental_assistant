#!/bin/bash

# Скрипт для проверки приложения без запуска Docker

echo "Проверка приложения dental_assistant..."

# Проверяем наличие всех необходимых файлов
echo -e "\n> Проверка структуры проекта:"

REQUIRED_FILES=(
  "frontend/app.py"
  "frontend/report_generator.py"
  "frontend/models/all_models.py"
  "requirements.txt"
  "Dockerfile"
  "docker-compose.yml"
)

ALL_OK=true

for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file найден"
  else
    echo "❌ $file не найден"
    ALL_OK=false
  fi
done

# Проверяем наличие каталогов
REQUIRED_DIRS=(
  "frontend"
  "frontend/models"
  "procedures"
  "prompts"
)

for dir in "${REQUIRED_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    echo "✅ Каталог $dir найден"
  else
    echo "❌ Каталог $dir не найден"
    ALL_OK=false
  fi
done

if [ "$ALL_OK" = true ]; then
  echo -e "\n✅ Структура проекта в порядке"
else
  echo -e "\n❌ Обнаружены проблемы со структурой проекта"
  exit 1
fi

# Проверяем импорт Python-модулей
echo -e "\n> Проверка импорта Python-модулей:"
if command -v python3 &> /dev/null; then
  PYTHON_CMD="python3"
else
  PYTHON_CMD="python"
fi

$PYTHON_CMD -c "import sys; print(f'Используется Python {sys.version}')"

CHECK_IMPORT="
try:
    print('Проверка импорта модулей...')
    import sys
    sys.path.append('.')
    
    # Импортируем модули напрямую из all_models
    print('Импорт моделей из frontend.models.all_models...')
    from frontend.models.all_models import BaseReport
    print('✅ BaseReport импортирован успешно')
    
    # Импортируем report_generator
    print('Импорт report_generator...')
    from frontend import report_generator
    print('✅ report_generator импортирован успешно')
    
    # Проверяем импорт app.py
    print('Импорт app...')
    from frontend import app 
    print('✅ app импортирован успешно')
    
    print('Все модули успешно импортированы')
except Exception as e:
    print(f'❌ Ошибка импорта: {e}')
    sys.exit(1)
"

$PYTHON_CMD -c "$CHECK_IMPORT"

echo -e "\n✅ Проверка приложения dental_assistant завершена успешно!"
echo "Для запуска приложения выполните: ./deploy.sh" 