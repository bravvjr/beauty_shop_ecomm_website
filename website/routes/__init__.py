from flask import Blueprint

# Import blueprints from different route files
from .mpesa_routes import mpesa_bp
from .auth_routes import auth_bp
from .product_routes import product_bp

# Create a Blueprint to group all routes
routes_bp = Blueprint("routes", __name__)

# Register blueprints
routes_bp.register_blueprint(mpesa_bp, url_prefix="/mpesa")
routes_bp.register_blueprint(auth_bp, url_prefix="/auth")
routes_bp.register_blueprint(product_bp, url_prefix="/products")
