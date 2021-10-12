import pika
import json
from main.settings import AMQP_URL

params = pika.URLParameters(AMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    prop = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key="admin_2_web_mq",
        body=json.dumps(body),
        properties=prop
    )
