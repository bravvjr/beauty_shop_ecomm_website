from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm, PasswordChangeForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user


auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            # Check if the email already exists
            existing_customer = Customer.query.filter_by(email=email).first()
            if existing_customer:
                flash('Account Not Created!!, Email already exists')
                return redirect('/sign-up')

            # Create a new customer
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = password2  # This will hash the password

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account Created Successfully, You can now Login')
                return redirect('/login')
            except Exception as e:
                db.session.rollback()  # Rollback the transaction in case of an error
                print(f"Error: {e}")  # Print the full error message
                flash('An error occurred while creating the account. Please try again.')
        else:
            flash('Passwords do not match!!')

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                flash('Logged in successfully!')
                return redirect('/')
            else:
                flash('Incorrect Email or Password')
        else:
            flash('Account does not exist. Please Sign Up.')

    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')

@auth.route('/user-profile')
@login_required
def user_profile():
    return render_template('user_profile.html')

@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    customer = Customer.query.get(customer_id)
    return render_template('profile.html', customer=customer)

@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    form = PasswordChangeForm()
    customer = Customer.query.get(customer_id)
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = confirm_new_password
                db.session.commit()
                flash('Password Updated Successfully')
                return redirect(f'/profile/{customer.id}')
            else:
                flash('New Passwords do not match!!')

        else:
            flash('Current Password is Incorrect')

    return render_template('change_password.html', form=form)

@auth.route('/wishlist')
@login_required
def wishlist():
    return render_template('wishlist.html')

@auth.route('/products')
@login_required
def products():
    return render_template('products.html', items=your_product_data)