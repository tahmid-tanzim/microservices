import pika

params = pika.URLParameters("amqps://mdheidwz:WEeFRGeW9XZSO1bjK2HC0uHh4P-Tf-38@codfish.rmq.cloudamqp.com/mdheidwz")
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish():
    channel.basic_publish(exchange="", routing_key="admin_mq", body="test publish hello")

