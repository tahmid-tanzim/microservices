import pika

params = pika.URLParameters("amqps://mdheidwz:WEeFRGeW9XZSO1bjK2HC0uHh4P-Tf-38@codfish.rmq.cloudamqp.com/mdheidwz")
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="web_mq")


def callback(ch, method, properties, body):
    print("\nReceived from web_mq")
    print(body, end="\n-----------------------------")


channel.basic_consume(queue="web_mq", on_message_callback=callback, auto_ack=True)
print("Started consuming")
channel.start_consuming()
channel.close()