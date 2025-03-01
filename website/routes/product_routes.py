from flask import Blueprint, request, jsonify
from website.models import db, Product

product_bp = Blueprint("product", __name__)

@product_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]
    return jsonify(product_list), 200

@product_bp.route("/", methods=["POST"])
def add_product():
    data = request.get_json()
    new_product = Product(name=data["name"], price=data["price"], stock=data["stock"])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added successfully!"}), 201
