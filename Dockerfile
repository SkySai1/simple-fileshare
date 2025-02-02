# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Обновляем pip перед установкой зависимостей
RUN pip install --no-cache-dir --upgrade pip

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаем папку для файлов (если её нет)
RUN mkdir -p /app/files

# Открываем порт 5000
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]
