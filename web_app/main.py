import requests
from dataclasses import dataclass
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint("user_id", "product_id", name="user_product_unique")


@app.route("/api/products")
def index():
    products = Product.query.all()
    return jsonify(products)


@app.route("/api/products/<int:id>/like", methods=["post"])
def like(id):
    print("Product ID", id)
    request = requests.get("http://docker.for.mac.localhost:8000/api/user")
    return request.json()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
