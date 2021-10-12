import requests
import os
from dataclasses import dataclass
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import UniqueConstraint
from dotenv import load_dotenv
from producer import publish

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")

CORS(app)
db = SQLAlchemy(app)
admin = {
    "host": os.getenv("ADMIN_HOST"),
    "port": os.getenv("ADMIN_PORT")
}


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    __table_args__ = (db.UniqueConstraint("user_id", "product_id", name="user_product_unique"),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)


@app.route("/api/products")
def index():
    products = Product.query.all()
    return jsonify(products), 200


@app.route("/api/products/<int:productId>/like", methods=["post"])
def like(productId):
    product = Product.query.get(productId)
    if product is None:
        return jsonify({
            "message": f"Sorry! Product ID ({productId}) DoesNotExist"
        }), 404

    # TODO -  Error handle required for HTTP request
    request = requests.get(f"http://{admin['host']}:{admin['port']}/api/user")
    user = request.json()

    try:
        productUser = ProductUser(user_id=user["id"], product_id=productId)
        db.session.add(productUser)
        db.session.commit()

        # Send Event to Admin
        publish("PRODUCT_LIKED", {"id": productId})
    except BaseException as e:
        # TODO - user_id & product_id unique constraints is NOT working.
        print(e.message, e.args)
        return jsonify({
            "message": f"Sorry! User-{user['id']} already liked Product-{productId}"
        }), 400

    return jsonify({
        "message": f"User ID ({user['id']}) liked Product ID ({productId})"
    }), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
