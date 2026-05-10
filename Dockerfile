FROM python:3.9-slim

WORKDIR /app

# Устанавливаем зависимости для MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости Python
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY app/ .

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]
