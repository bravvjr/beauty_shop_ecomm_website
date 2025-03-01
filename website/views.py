from flask import Blueprint, render_template, flash, redirect, request, jsonify
# from .models import Product, Cart, Order, Wishlist
from flask_login import login_required, current_user
# from . import db
import os
import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth
from website.models import Product, Cart, Order
from website import db


views = Blueprint("views", __name__)

# Load API credentials from .env
MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
MPESA_CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")

# URLs
MPESA_AUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
MPESA_STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"


def get_access_token():
    """Generate M-Pesa access token."""
    response = requests.get(
        MPESA_AUTH_URL, auth=HTTPBasicAuth(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET)
    )
    return response.json().get("access_token")


def stk_push(phone, amount, account_ref="OrderPayment"):
    """Initiate STK Push Payment"""
    access_token = get_access_token()
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{MPESA_SHORTCODE}{MPESA_PASSKEY}{timestamp}".encode()
    ).decode("utf-8")

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": MPESA_CALLBACK_URL,
        "AccountReference": account_ref,
        "TransactionDesc": "Payment for goods",
    }

    try:
        response = requests.post(MPESA_STK_URL, json=payload, headers=headers)
        response_data = response.json()

        print(f"STK Push Response: {response_data}")  # Log response for debugging

        return response_data
    except requests.exceptions.RequestException as e:
        print(f"Error with STK Push: {e}")
        return {"error": str(e)}


@views.route("/")
def home():
    items = Product.query.filter_by(flash_sale=True).all()
    return render_template(
        "home.html",
        items=items,
        cart=Cart.query.filter_by(customer_link=current_user.id).all()
        if current_user.is_authenticated
        else [],
    )


@views.route("/products")
def products():
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    category_id = request.args.get("category_id", type=int)
    flash_sale = request.args.get("flash_sale", type=bool)

    # Start with a base query
    query = Product.query
    if min_price is not None:
        query = query.filter(Product.current_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.current_price <= max_price)
    if category_id is not None:
        query = query.filter_by(category_id=category_id)
    if flash_sale is not None:
        query = query.filter_by(flash_sale=flash_sale)
    else:
        # Exclude flash_sale items by default if no filter is applied
        query = query.filter_by(flash_sale=False)

    return render_template("products.html", products=query.all())


@views.route("/add-to-cart/<int:item_id>")
@login_required
def add_to_cart(item_id):
    item = Product.query.get(item_id)
    existing_cart_item = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
    else:
        new_cart_item = Cart(product_link=item.id, customer_link=current_user.id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()
    flash(f"{item.product_name} added to cart")
    return redirect(request.referrer)


@views.route("/cart")
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)
    return render_template("cart.html", cart=cart, amount=amount, total=amount + 200)


@views.route("/place-order", methods=["POST"])
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if not customer_cart:
        flash("Your cart is empty")
        return redirect("/cart")

    total_amount = sum(item.product.current_price * item.quantity for item in customer_cart) + 200
    phone_number = request.form.get("phone_number")

    if not phone_number:
        flash("Please provide a phone number")
        return redirect("/cart")

    try:
        response = stk_push(phone_number, total_amount)

        # If there is an error in the response
        if "error" in response:
            flash(f"Payment initiation failed: {response['error']}")
            return redirect("/cart")

        for item in customer_cart:
            order = Order(
                quantity=item.quantity,
                price=item.product.current_price,
                status=response.get("ResponseCode", "Pending"),
                payment_id=response.get("MerchantRequestID"),
                product_link=item.product_link,
                customer_link=item.customer_link,
            )
            db.session.add(order)
            product = Product.query.get(item.product_link)
            product.in_stock -= item.quantity
            db.session.delete(item)

        db.session.commit()
        flash("Order placed successfully! Complete the payment on your phone.")
        return redirect("/orders")

    except Exception as e:
        print(e)
        flash("Order could not be placed.")
        return redirect("/cart")


@views.route("/orders")
@login_required
def orders():
    user_orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template("orders.html", orders=user_orders)


@views.route("/search", methods=["POST"])
def search():
    search_query = request.form.get("search")
    items = Product.query.filter(Product.product_name.ilike(f"%{search_query}%")).all()
    return render_template(
        "search.html",
        items=items,
        cart=Cart.query.filter_by(customer_link=current_user.id).all()
        if current_user.is_authenticated
        else [],
    )


@views.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():
    data = request.json
    print(f"Callback data: {data}")  # Log the callback data for debugging

    # Handle the callback and update the order status based on the response
    payment_status = data.get("ResultCode")
    payment_id = data.get("MerchantRequestID")

    order = Order.query.filter_by(payment_id=payment_id).first()
    if order:
        if payment_status == "0":  # Payment successful
            order.status = "Paid"
        else:
            order.status = "Failed"
        db.session.commit()

    return jsonify({"status": "success"}), 200


@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@views.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
