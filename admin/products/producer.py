import pika
import json

params = pika.URLParameters("amqps://mdheidwz:WEeFRGeW9XZSO1bjK2HC0uHh4P-Tf-38@codfish.rmq.cloudamqp.com/mdheidwz")
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    prop = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key="web_mq",
        body=json.dumps(body),
        properties=prop
    )
