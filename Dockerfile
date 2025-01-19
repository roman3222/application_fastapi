FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем пакет application в PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Запускаем приложение
CMD ["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "80"]