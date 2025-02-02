# Используем базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir flask

# Открываем порт 5000
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]
