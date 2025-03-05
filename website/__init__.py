from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from pathlib import Path
from website.config import Config

# Load environment variables from .env file
dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object

    # Load configuration
    app.config.from_object('website.config.Config')

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Set the login view for Flask-Login
    


    # Error handler for 404
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    # Error handler for 500 (Internal Server Error)
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        """
        Callback to reload the user object from the user ID stored in the session.
        """
        from .models import Customer  # Import here to avoid circular imports
        return Customer.query.get(int(id))

    # Import and register blueprints
    from .views import views
    from .auth import auth  # type: ignore
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # Create database tables (for development only)
    with app.app_context():
        db.create_all()

    return app
