from sqlalchemy import Enum
from . import db
from flask_login import UserMixin
from sqlalchemy import JSON
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from website import db

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationships
    cart_items = db.relationship('Cart', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='customer', lazy=True)
    wishlist_items = db.relationship('Wishlist', backref='customer', lazy=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Customer {self.username}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    products = db.relationship('Product', back_populates='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float)
    in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000))
    flash_sale = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=True)

    # Relationships
    carts = db.relationship('Cart', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)
    wishlist_items = db.relationship('Wishlist', backref='product', lazy=True)
    category = db.relationship('Category', back_populates='products')

    def __repr__(self):
        return f'<Product {self.product_name}>'


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Foreign Keys
    customer_link = db.Column(
        db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(
        db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Cart {self.id}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.JSON, nullable=False)  # Stores product details
    status = db.Column(db.String(100), nullable=False, default='pending')
    payment_id = db.Column(db.String(1000))
    phone_number = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    # Define a relationship to the Customer model
    customer = db.relationship('Customer', backref='orders')

    def __repr__(self):
        return f'<Order {self.id}>'

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_link = db.Column(
        db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(
        db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Wishlist {self.id}>'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date_reviewed = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    customer_link = db.Column(
        db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(
        db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Review {self.id}>'


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(Enum(
        'credit_card', 'paypal', 'bank_transfer', name='payment_method_enum'), nullable=False)
    status = db.Column(Enum('pending', 'completed', 'failed',
                           name='payment_status_enum'), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    order = db.relationship('Order', backref='payments')
    customer = db.relationship('Customer', backref='payments')

    def __repr__(self):
        return f'<Payment {self.id}>'