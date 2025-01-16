import json
from schemas import Application
from aiokafka import AIOKafkaProducer

async def send_to_kafka(application: Application):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v.dict()).encode('utf-8')
    )
    await producer.start()
    try:
        await producer.send('applications', application)
    finally:
        await producer.stop()