from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange, Email, Length
from flask_wtf.file import FileField, FileRequired
from wtforms import FileField, BooleanField,  TextAreaField
from werkzeug.utils import secure_filename
from website.models import Category





class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), length(min=2)])
    password1 = PasswordField('Enter Your Password', validators=[
                              DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[
                              DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password',
                             validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[
                                     DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[
                                 DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
                                         DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')


class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[
                            DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Product Picture', validators=[DataRequired()])
    description = TextAreaField('Product Description', validators=[DataRequired()])
    flash_sale = BooleanField('Flash Sale')
    category_id = SelectField('Category', coerce=int,
                              validators=[DataRequired()])

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update')
    
    def __init__(self, *args, **kwargs):
        super(ShopItemsForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(category.id, category.name)
                                    for category in Category.query.all()]


class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'),
                                                        ('Out for delivery',
                                                         'Out for delivery'),
                                                        ('Delivered', 'Delivered'), ('Canceled', 'Canceled')])

    update = SubmitField('Update Status')
    

class CategoryForm(FlaskForm):
    name = StringField(
        'Category Name',
        validators=[
            DataRequired(message="Category name is required."),
            Length(min=2, max=50,
                   message="Category name must be between 2 and 50 characters.")
        ]
    )
    submit = SubmitField('ADD Category')
