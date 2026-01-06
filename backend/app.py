from flask import Flask, jsonify
from backend.config import Config
from backend.models import db
from backend.routes.products import create_product
from backend.routes.alerts import low_stock_alerts

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/')
    def home():
        return {
            "message": "StockFlow API",
            "endpoints": {
                "GET /api/companies/<company_id>/alerts/low-stock": "Get low stock alerts for a company",
                "POST /api/products": "Create a new product"
            }
        }
        

    app.add_url_rule('/api/products', view_func=create_product, methods=['POST'])
    app.add_url_rule(
        '/api/companies/<int:company_id>/alerts/low-stock',
        view_func=low_stock_alerts,
        methods=['GET']
    )

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)