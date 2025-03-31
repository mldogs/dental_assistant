#!/bin/bash

# Скрипт для проверки статуса стоматологического приложения
echo "Проверка статуса приложения..."

# Проверяем, запущено ли приложение
if docker ps | grep -q dental-app; then
    echo "✅ Приложение запущено"
    
    # Получаем информацию о контейнере
    CONTAINER_ID=$(docker ps | grep dental-app | awk '{print $1}')
    echo "ID контейнера: $CONTAINER_ID"
    
    # Получаем информацию о ресурсах
    echo -e "\nИспользование ресурсов:"
    docker stats --no-stream $CONTAINER_ID
    
    # IP и порт
    IP=$(hostname -I | awk '{print $1}')
    echo -e "\nПриложение доступно по адресу: http://$IP:8501"
    
    # Проверяем доступность приложения
    echo -e "\nПроверка доступности..."
    if curl -s --head http://localhost:8501 | grep "200 OK" > /dev/null; then
        echo "✅ Приложение отвечает на запросы"
    else
        echo "⚠️ Приложение не отвечает на запросы"
    fi
    
    # Последние логи
    echo -e "\nПоследние логи приложения:"
    docker logs --tail 20 $CONTAINER_ID
else
    echo "❌ Приложение не запущено"
    
    # Проверяем образ
    if docker images | grep -q dental-app; then
        echo "✅ Docker образ существует"
    else
        echo "❌ Docker образ не найден"
    fi
    
    echo -e "\nДля запуска приложения выполните:"
    echo "  ./deploy.sh"
fi 