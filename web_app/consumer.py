import pika
import json
from main import Product, db

params = pika.URLParameters("amqps://mdheidwz:WEeFRGeW9XZSO1bjK2HC0uHh4P-Tf-38@codfish.rmq.cloudamqp.com/mdheidwz")
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="admin_2_web_mq")


def callback(ch, method, properties, body):
    print("\nReceived from admin_2_web_mq")
    data = json.loads(body)

    if properties.content_type == "PRODUCT_CREATED":
        print("PRODUCT_CREATED")
        product = Product(
            id=data["id"],
            title=data["title"],
            image=data["image"]
        )
        if product is not None:
            db.session.add(product)
            db.session.commit()
        else:
            print("Sorry! Product cannot be created", data)

    if properties.content_type == "PRODUCT_UPDATED":
        print("PRODUCT_UPDATED")
        product = Product.query.get(data["id"])
        if product is not None:
            product.title = data["title"]
            product.image = data["image"]
            db.session.commit()
        else:
            print("Sorry! Product DoesNotExist", data["id"])

    if properties.content_type == "PRODUCT_DELETED":
        print("PRODUCT_DELETED")
        product = Product.query.get(data["id"])
        if product is not None:
            db.session.delete(product)
            db.session.commit()
        else:
            print("Sorry! Product DoesNotExist", data["id"])


channel.basic_consume(queue="admin_2_web_mq", on_message_callback=callback, auto_ack=True)
print("Started consuming")
channel.start_consuming()
channel.close()
