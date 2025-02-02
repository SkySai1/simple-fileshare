# Используем официальный образ Python 3.10
FROM python:3.10

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт (по умолчанию Gunicorn использует 8000)
EXPOSE 8000

# Запуск приложения через Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
