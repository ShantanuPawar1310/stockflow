from flask import request, jsonify
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from backend.models import db, Product, Inventory

def create_product():
    data = request.json or {}

    required_fields = ['name', 'sku', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        price = Decimal(str(data['price']))
    except:
        return jsonify({"error": "Invalid price format"}), 400

    try:
        with db.session.begin():

            if Product.query.filter_by(sku=data['sku']).first():
                return jsonify({"error": "SKU already exists"}), 409

            product = Product(
                name=data['name'],
                sku=data['sku'],
                price=price
            )
            db.session.add(product)
            db.session.flush()

            if 'warehouse_id' in data:
                inventory = Inventory(
                    product_id=product.id,
                    warehouse_id=data['warehouse_id'],
                    quantity=data.get('initial_quantity', 0)
                )
                db.session.add(inventory)

        return jsonify({"product_id": product.id}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 400