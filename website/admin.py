from flask import Blueprint, render_template, flash, redirect, request, send_from_directory, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer, Cart, Inventory, Category, Payment
from . import db
from datetime import datetime
from .forms import ShopItemsForm, OrderForm


admin = Blueprint('admin', __name__)


@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id != 1:
        return render_template('404.html'), 403

    form = ShopItemsForm()
    if form.validate_on_submit():
        product_name = form.product_name.data
        description = form.description.data  # Fetch description from form
        current_price = form.current_price.data
        previous_price = form.previous_price.data
        in_stock = form.in_stock.data
        flash_sale = form.flash_sale.data
        file = form.product_picture.data

        file_name = secure_filename(file.filename)
        file_path = f'./media/{file_name}'
        file.save(file_path)

        new_product = Product(
            product_name=product_name,
            description=description,  # Save description
            current_price=current_price,
            previous_price=previous_price,
            in_stock=in_stock,
            flash_sale=flash_sale,
            product_picture=file_path
        )

        try:
            db.session.add(new_product)
            db.session.commit()
            flash(f'{product_name} added successfully!', 'success')
            return redirect('/shop-items')
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash('Failed to add product. Please try again.', 'danger')

    return render_template('add_shop_items.html', form=form)

@admin.route('/shop-items')
@login_required
def shop_items():
    if current_user.id != 1:
        return render_template('404.html'), 403

    items = Product.query.order_by(Product.date_added).all()
    return render_template('shop_items.html', items=items)


@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id != 1:
        return render_template('404.html'), 403

    item_to_update = Product.query.get_or_404(item_id)
    form = ShopItemsForm(obj=item_to_update)

    if form.validate_on_submit():
        form.populate_obj(item_to_update)
        file = form.product_picture.data

        if file:
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)
            item_to_update.product_picture = file_path

        try:
            db.session.commit()
            flash(f'{item_to_update.product_name} updated successfully!', 'success')
            return redirect('/shop-items')
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash('Failed to update product. Please try again.', 'danger')

    return render_template('update_item.html', form=form, item=item_to_update)


@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1:
        try:
            # Find the product to delete
            item_to_delete = Product.query.get_or_404(item_id)

            # Delete all related rows in the cart table
            Cart.query.filter_by(product_link=item_id).delete()

            # Delete the product
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Product and related cart items deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash(f'Failed to delete product. Error: {e}', 'danger')
        return redirect('/shop-items')
    return render_template('404.html'), 403

@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.id != 1:
        return render_template('404.html'), 403

    orders = Order.query.all()
    return render_template('view_orders.html', orders=orders)


@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id != 1:
        return render_template('404.html'), 403

    order = Order.query.get_or_404(order_id)
    form = OrderForm(obj=order)

    if form.validate_on_submit():
        form.populate_obj(order)
        try:
            db.session.commit()
            flash(f'Order {order_id} updated successfully!', 'success')
            return redirect('/view-orders')
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash('Failed to update order. Please try again.', 'danger')

    return render_template('order_update.html', form=form, order=order)


@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id != 1:
        return render_template('404.html'), 403

    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)


@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id != 1:
        return render_template('404.html'), 403

    return render_template('admin.html')

@admin.route('/inventory')
def inventory():
    inventory = Product.query.with_entities(
        Product.id, Product.product_name, Product.category_id, Product.in_stock, Product.date_added
    ).all()
    return render_template('inventory.html', inventory=inventory)


@admin.route('/edit-inventory/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_inventory(id):
    if current_user.id != 1: 
        return render_template('404.html'), 403

    item = Inventory.query.get_or_404(id) 

    if request.method == 'POST':
        item.product_name = request.form['product_name']
        item.category_id = request.form['category_id']
        item.stock = int(request.form['stock'])
        item.updated_at = datetime.utcnow() 

        try:
            db.session.commit()
            flash('Inventory item updated successfully!', 'success')
            return redirect(url_for('inventory'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update inventory item. Please try again.', 'danger')
            print(f"Error: {e}")

    return render_template('edit_inventory.html', item=item)


@admin.route('/categories')
@login_required
def categories():
    if current_user.id != 1:  
        return render_template('404.html'), 403

    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10  

    query = Category.query
    if search_query:
        query = query.filter(Category.name.ilike(f'%{search_query}%'))

    categories = query.order_by(Category.created_at.desc()).paginate(
        page=page, per_page=per_page)

    return render_template('categories.html', categories=categories, search_query=search_query)


@admin.route('/payments')
@login_required
def payments():
    if current_user.id != 1:  
        return render_template('404.html'), 403

    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10  


    query = Payment.query
    if search_query:
        query = query.filter(Payment.transaction_id.ilike(f'%{search_query}%'))


    payments = query.order_by(Payment.created_at.desc()).paginate(
        page=page, per_page=per_page)

    return render_template('payments.html', payments=payments, search_query=search_query)


@admin.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        print(request.form)  # Debug: Ensure description is received

        new_description = request.form.get('description')
        print(f"Updating description: {new_description}")  # Debug

        if new_description:
            product.description = new_description
            db.session.add(product)  # Ensure object is marked as changed
            db.session.commit()
            db.session.refresh(product)  # Ensure data is fetched from DB
            print(f"Saved Description: {product.description}")  # Debug

            flash('Product description updated successfully!', 'success')
            return redirect(url_for('shop_items'))

    return render_template('edit_product.html', product=product)
