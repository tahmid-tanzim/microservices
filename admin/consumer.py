import os
import django
import pika
import json

# Setup Django to load Model
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()
from products.models import Product

params = pika.URLParameters("amqps://mdheidwz:WEeFRGeW9XZSO1bjK2HC0uHh4P-Tf-38@codfish.rmq.cloudamqp.com/mdheidwz")
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="web_2_admin_mq")


def callback(ch, method, properties, body):
    print("\nReceived from web_2_admin_mq")
    data = json.loads(body)
    if properties.content_type == "PRODUCT_LIKED":
        print("PRODUCT_LIKED")
        product = Product.objects.get(id=data["id"])
        if product is not None:
            product.likes = product.likes + 1
            product.save()
        else:
            print("Sorry! Product DoesNotExist", data["id"])


channel.basic_consume(queue="web_2_admin_mq", on_message_callback=callback, auto_ack=True)
print("Started consuming")
channel.start_consuming()
channel.close()
