# Application Service

Этот проект представляет собой сервис для управления заявками, построенный на базе FastAPI, PostgreSQL и Kafka. Сервис позволяет создавать новые заявки, получать список заявок с возможностью фильтрации и пагинации, а также отправлять заявки в Kafka для дальнейшей обработки.

## Основные функции

- **Создание заявки**: Позволяет создать новую заявку с указанием имени пользователя и описания.
- **Получение списка заявок**: Возвращает список заявок с возможностью фильтрации по имени пользователя и пагинацией.
- **Интеграция с Kafka**: Каждая созданная заявка отправляется в Kafka для дальнейшей обработки.

## Технологии

- **FastAPI**: Веб-фреймворк для создания API.
- **PostgreSQL**: Реляционная база данных для хранения заявок.
- **Kafka**: Система потоковой обработки данных для асинхронной обработки заявок.
- **SQLAlchemy**: ORM для работы с базой данных.
- **Docker**: Контейнеризация приложения и зависимостей.

## Установка и запуск

### Требования

- Docker
- Docker Compose

### Запуск приложения

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/application-service.git
   cd application-service
   
2. Создайте файл .env в корне проекта и заполните его переменными окружения:
* DB_USER=your_db_user
* DB_PASSWORD=your_db_password
* DB_HOST=db
* DB_PORT=5432
* DB_NAME=your_db_name
* KAFKA_BOOTSTRAP_SERVERS=kafka:9092
* KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
* ALLOW_PLAINTEXT_LISTENER=yes
* ALLOW_ANONYMOUS_LOGIN=yes

3. Запустите приложение с помощью Docker Compose:

    ```bash
   docker-compose up
   

### Пимеры запросов

#### Создание заявки

    curl -X POST "http://localhost:80/applications/" -H "Content-Type: application/json" -d '{"user_name": "Ivanov Ivan", "description": "Some description"}'

### API Документация

* Swagger UI: http://localhost:80/docs
* ReDoc: http://localhost:80/redoc