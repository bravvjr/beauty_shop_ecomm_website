from flask import Blueprint, render_template, flash, redirect, request, jsonify, url_for
from .models import Product, Cart, Order, Wishlist
from flask_login import login_required, current_user
from . import db
from intasend import APIService


views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'ISPubKey_test_6fdcc500-15b3-476a-b5fc-9bc4f4523390'

API_TOKEN = 'ISSecretKey_test_a99a507f-e552-497d-a4fb-5b6e13f4bf9d'


@views.route('/')
def home():

    items = Product.query.filter_by(flash_sale=True)

    return render_template('home.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])


@views.route('/products')
def products():
    # Get filter parameters from the request
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    category_id = request.args.get('category_id', type=int)
    flash_sale = request.args.get('flash_sale', type=bool)

    # Start with a base query
    query = Product.query

    # Apply filters based on request parameters
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

    # Fetch filtered products
    filtered_products = query.all()

    return render_template('products.html', products=filtered_products)

@views.route('/product-section')
def product_section():
    # Get the maximum price from the request (default to None if not provided)
    max_price = request.args.get('max_price', type=float)

    # Fetch the maximum price from the database to set the slider's max value
    max_product_price = db.session.query(db.func.max(Product.current_price)).scalar() or 10000

    # Start with a base query excluding flash_sale items
    query = Product.query.filter_by(flash_sale=False)

    # Apply price filter if max_price is provided
    if max_price is not None:
        query = query.filter(Product.current_price <= max_price)

    # Fetch filtered products
    items = query.all()

    return render_template('product_section.html', items=items, max_price=max_product_price)

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    
    # Check if the item is out of stock
    if item_to_add.in_stock <= 0:
        flash(f'{item_to_add.product_name} is out of stock and cannot be added to the cart.')
        return redirect(request.referrer)
    
    item_exists = Cart.query.filter_by(
        product_link=item_id, customer_link=current_user.id).first()
    
    if item_exists:
        try:
            # Check if adding more items exceeds the available stock
            if item_exists.quantity + 1 > item_to_add.in_stock:
                flash(f'Cannot add more {item_to_add.product_name} to the cart. Only {item_to_add.in_stock} items are available.')
                return redirect(request.referrer)
            
            item_exists.quantity = item_exists.quantity + 1
            db.session.commit()
            flash(f'Quantity of {item_exists.product.product_name} has been updated')
            return redirect(request.referrer)
        except Exception as e:
            print('Quantity not Updated', e)
            flash(f'Quantity of {item_exists.product.product_name} not updated')
            return redirect(request.referrer)

    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.product_name} added to cart')
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.product.product_name} has not been added to cart')

    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.product.current_price * item.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount)


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity + 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)

@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)

        if cart_item and cart_item.quantity > 0:
            cart_item.quantity -= 1
            db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)

        data = {
            'quantity': cart_item.quantity if cart_item else 0,
            'amount': amount,
            'total': amount + 200
        }
        return jsonify(data)  # Ensure you return a response


        return jsonify(data)


@views.route('removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)

@views.route('/payment-successful')
def payment_successful():
    # Get the payment ID or checkout ID from the query parameters
    payment_id = request.args.get('payment_id') or request.args.get('checkout_id')
    print("Payment ID from IntaSend:", payment_id)  # Debugging: Check if this is received

    if payment_id:
        # Find the order in the database using the payment_id
        order = Order.query.filter_by(payment_id=payment_id).first()

        if order:
            # Update the order status to 'paid'
            order.status = 'paid'
            db.session.commit()

            # Render the payment_successful page with the order details
            return render_template('payment_successful.html', order=order)

    # If no payment ID or order is found, redirect to home
    flash('Invalid payment details.')
    return redirect('/')

@views.route('/confirm-payment', methods=['POST'])
@login_required
def confirm_payment():
    # Get the payment ID from the form
    payment_id = request.form.get('payment_id')

    if payment_id:
        # Find the order in the database using the payment_id
        order = Order.query.filter_by(payment_id=payment_id).first()

        if order:
            # Update the order status to 'paid'
            order.status = 'PAID'
            db.session.commit()
            flash('Payment confirmed! Thank you for your purchase.')
        else:
            flash('Order not found.')
    else:
        flash('Invalid payment details.')

    # Redirect to the orders page
    return redirect(url_for('views.orders'))

@views.route('/place-order', methods=['POST'])
@login_required
def place_order():
    phone_number = request.form.get('phone_number')

    # Validate the phone number
    if not phone_number or not phone_number.startswith('254') or len(phone_number) != 12:
        flash('Invalid phone number. Please enter a valid Kenyan phone number (e.g., 2547XXXXXXXX).')
        return redirect('/cart')

    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if customer_cart:
        try:
            # Calculate the total amount
            total = 0
            items = []  # List to store product details

            for item in customer_cart:
                total += item.product.current_price * item.quantity
                items.append({
                    'product_id': item.product_link,
                    'product_name': item.product.product_name,
                    'quantity': item.quantity,
                    'price': item.product.current_price
                })

            # Initialize IntaSend service
            service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)

            # Generate a checkout link
            redirect_url = url_for('views.payment_successful', _external=True)
            print("Redirect URL:", redirect_url)  # Debugging: Print the redirect URL

            response = service.collect.checkout(
                phone_number=phone_number,
                email=current_user.email,
                amount=15,  # Testing amount
                currency='KES',
                comment='Purchase of goods',
                redirect_url=redirect_url,
                api_ref=f'order_{current_user.id}',
            )
            print("IntaSend Response:", response)  # Debugging: Print the full response

            # Create a single order in the database
            new_order = Order(
                items=items,
                status='PENDING',
                payment_id=response.get('id'),
                phone_number=phone_number,
                customer_link=current_user.id
            )
            db.session.add(new_order)

            # Update product stock and remove items from cart
            for item in customer_cart:
                product = Product.query.get(item.product_link)
                product.in_stock -= item.quantity
                db.session.delete(item)

            # Commit changes to the database
            db.session.commit()

            # Redirect the customer to the payment URL
            return redirect(response.get('url'))

        except Exception as e:
            print('Error generating payment link:', str(e))  # Log the full error message
            db.session.rollback()  # Rollback in case of error
            flash('Failed to generate payment link. Please try again.')
            return redirect('/cart')
    else:
        flash('Your cart is empty.')
        return redirect('/cart')

@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(
            Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                               if current_user.is_authenticated else [])


@views.route('/orders')
@login_required
def orders():
    # Fetch orders for the current user
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)

@views.route('/add-to-wishlist/<int:item_id>')
@login_required
def add_to_wishlist(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Wishlist.query.filter_by(
        product_link=item_id, customer_link=current_user.id).first()
    
    if item_exists:
        flash(f'{item_to_add.product_name} is already in your wishlist')
        return redirect(request.referrer)

    new_wishlist_item = Wishlist()
    new_wishlist_item.product_link = item_to_add.id
    new_wishlist_item.customer_link = current_user.id

    try:
        db.session.add(new_wishlist_item)
        db.session.commit()
        flash(f'{item_to_add.product_name} added to wishlist')
    except Exception as e:
        print('Item not added to wishlist', e)
        flash(f'{item_to_add.product_name} has not been added to wishlist')

    return redirect(request.referrer)

@views.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(customer_link=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@views.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@views.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

    return render_template('search.html')