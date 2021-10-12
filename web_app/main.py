import requests
from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:C0V1D19@db/microservice_web_db"
CORS(app)
db = SQLAlchemy(app)


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
    return jsonify(products)


@app.route("/api/products/<int:productId>/like", methods=["post"])
def like(productId):
    request = requests.get("http://docker.for.mac.localhost:8000/api/user")
    user = request.json()

    try:
        productUser = ProductUser(
            user_id=user["id"],
            product_id=productId
        )
        db.session.add(productUser)
        db.session.commit()

        # Send Event to Admin
        publish("PRODUCT_LIKED", {"id": productId})
    except:
        abort(400, f"Sorry! User-{user['id']} already liked Product-{productId}")

    return jsonify({
        "message": f"You've liked product ID {productId}"
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
