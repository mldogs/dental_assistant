FROM python:3.10-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install streamlit

# Копируем все файлы проекта
COPY . .

# Переменные окружения по умолчанию
ENV PORT=8501
ENV HOST=0.0.0.0

# Открываем порт
EXPOSE 8501

# Запускаем приложение
CMD streamlit run frontend/app.py --server.port $PORT --server.address $HOST 