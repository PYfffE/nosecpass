# Используем официальный образ Python
FROM python:3.8-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY app/ .

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP app.py

# Запускаем Flask приложение
CMD ["flask", "run", "--host=0.0.0.0"]