from datetime import datetime, timedelta
from sqlalchemy import func
from flask import jsonify

from backend.models import (
    db,
    Warehouse,
    Inventory,
    Product,
    Sales,
    Supplier,
    ProductSupplier
)

def low_stock_alerts(company_id):
    """
    Returns low-stock alerts for all warehouses under a company.
    """

    alerts = []

    # 1. Fetch warehouses for the company
    warehouses = Warehouse.query.filter_by(company_id=company_id).all()
    warehouse_ids = [w.id for w in warehouses]

    if not warehouse_ids:
        return jsonify({"alerts": [], "total_alerts": 0})

    # 2. Fetch inventory with related product and warehouse
    inventory_rows = (
        db.session.query(Inventory, Product, Warehouse)
        .join(Product, Inventory.product_id == Product.id)
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
        .filter(Inventory.warehouse_id.in_(warehouse_ids))
        .all()
    )

    for inventory, product, warehouse in inventory_rows:

        # 3. Recent sales in last 30 days
        recent_sales = (
            db.session.query(func.sum(Sales.quantity))
            .filter(
                Sales.product_id == product.id,
                Sales.warehouse_id == warehouse.id,
                Sales.sold_at >= datetime.utcnow() - timedelta(days=30)
            )
            .scalar()
        ) or 0

        # Skip if no recent sales
        if recent_sales == 0:
            continue

        # 4. Check low stock threshold
        if inventory.quantity >= product.low_stock_threshold:
            continue

        # 5. Days until stockout
        avg_daily_sales = recent_sales / 30
        days_until_stockout = (
            int(inventory.quantity / avg_daily_sales)
            if avg_daily_sales > 0 else None
        )

        # 6. Supplier info
        supplier = (
            Supplier.query
            .join(ProductSupplier)
            .filter(ProductSupplier.product_id == product.id)
            .first()
        )

        alerts.append({
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "current_stock": inventory.quantity,
            "threshold": product.low_stock_threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": {
                "id": supplier.id,
                "name": supplier.name,
                "contact_email": supplier.contact_email
            } if supplier else None
        })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })