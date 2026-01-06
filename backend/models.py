from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.BigInteger, primary_key=True)
    company_id = db.Column(db.BigInteger, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.Text)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.BigInteger, primary_key=True)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    low_stock_threshold = db.Column(db.Integer, default=10)
    product_type = db.Column(db.String(50), default='standard')


class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), nullable=False)
    warehouse_id = db.Column(db.BigInteger, db.ForeignKey('warehouse.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)

    __table_args__ = (
        db.UniqueConstraint('product_id', 'warehouse_id'),
    )


class Supplier(db.Model):
    __tablename__ = 'supplier'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255))


class ProductSupplier(db.Model):
    __tablename__ = 'product_supplier'
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), primary_key=True)
    supplier_id = db.Column(db.BigInteger, db.ForeignKey('supplier.id'), primary_key=True)


class Sales(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), nullable=False)
    warehouse_id = db.Column(db.BigInteger, db.ForeignKey('warehouse.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sold_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )