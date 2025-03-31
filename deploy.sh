#!/bin/bash

# Скрипт для деплоя стоматологического приложения
echo "Начинаем деплой приложения..."

# Проверяем наличие Docker и Docker Compose
if ! command -v docker &> /dev/null; then
    echo "Docker не установлен. Устанавливаем..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "Docker установлен."
else
    echo "Docker уже установлен."
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose не установлен. Устанавливаем..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose установлен."
else
    echo "Docker Compose уже установлен."
fi

# Проверяем наличие файла .env
if [ ! -f .env ]; then
    echo "Файл .env не найден. Копируем из example.env..."
    cp example.env .env
    echo "ВНИМАНИЕ: Отредактируйте файл .env и вставьте ваши API ключи."
    echo "После этого запустите скрипт заново."
    exit 1
fi

# Запускаем приложение
echo "Запускаем приложение через Docker Compose..."
docker-compose down
docker-compose up -d --build

# Проверяем статус
echo "Проверяем статус приложения..."
sleep 5
if docker ps | grep -q dental-app; then
    echo "✅ Приложение успешно запущено!"
    echo "Приложение доступно по адресу: http://$(hostname -I | awk '{print $1}'):8501"
else
    echo "❌ Ошибка при запуске приложения. Проверьте логи:"
    docker-compose logs
fi 