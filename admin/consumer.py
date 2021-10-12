import pika
import json
# Setup Django to load Model
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()
from products.models import Product
from main.settings import AMQP_URL

params = pika.URLParameters(AMQP_URL)
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
