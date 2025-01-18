import json
from schemas import Application
from aiokafka import AIOKafkaProducer
from config import settings
from log import info_logger, error_logger
from datetime import datetime


def datetime_serializer(obj: datetime) -> str:
    """
    Сериализует объект datetime в строку в формате ISO.
    :param obj: Объект типа данных datetime
    :return: Строковое представление объекта datetime в формате ISO.
    :raises: TypeError: Если объект не является экземпляром datetime.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


async def send_to_kafka(application: Application) -> None:
    """
    Отправляет заявку в Kafka.
    :param application: (models.Application): Заявка для отправки.
    :raises: KafkaError: Если произошла ошибка при отправке сообщения в Kafka.
    """
    application_schema = Application.model_validate(application)
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.get_kafka_server(),
        value_serializer=lambda v: json.dumps(v.model_dump(), default=datetime_serializer).encode('utf-8')
    )
    try:
        info_logger.info(f"Starting Kafka producer for application ID: {application_schema.id}")
        await producer.start()
        info_logger.info(f"Sending application to Kafka: {application_schema.id}")
        await producer.send('applications', application_schema)
        info_logger.info(f"Application successfully sent to Kafka: {application_schema.id}")
    except Exception as error:
        error_logger.error(f"Failed to send application to Kafka: {application_schema.id}. Error: {error}")
        raise
    finally:
        info_logger.info(f"Stopping Kafka producer for application ID: {application_schema.id}")
        await producer.stop()