import asyncio
from aiokafka import AIOKafkaConsumer
from application.log import info_logger
from application.config import settings

async def consume_messages():
    consumer = AIOKafkaConsumer(
        'applications',
        bootstrap_servers=settings.get_kafka_server(),
        group_id="test-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            info_logger.info(f"Kafka: получено сообщение -> {msg.value}")
    finally:
        await consumer.stop()


asyncio.run(consume_messages())