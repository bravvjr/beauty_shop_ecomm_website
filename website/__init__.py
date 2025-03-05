from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env file
dotenv_path = Path(__file__).parent.parent / '.env'  
load_dotenv(dotenv_path=dotenv_path)

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Flask-Login
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Set configuration from environment variables
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hbnwdvbn ajnbsjn ahe') #render secret key error fallback
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize Flask-Login with the app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Error handler for 404
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        from .models import Customer  # Import here to avoid circular imports
        return Customer.query.get(int(id))

    # Import and register blueprints
    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    return app