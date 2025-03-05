import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Log database environment variables for debugging
logging.info(f"DB_USER: {os.getenv('DB_USER')}")
logging.info(f"DB_HOST: {os.getenv('DB_HOST')}")
logging.info(f"DB_PORT: {os.getenv('DB_PORT')}")
logging.info(f"DB_NAME: {os.getenv('DB_NAME')}")

# Validate required environment variables
required_vars = ['DB_USER', 'DB_PASSWORD',
                 'DB_HOST', 'DB_PORT', 'DB_NAME', 'SECRET_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise ValueError(
        f"Missing environment variables: {', '.join(missing_vars)}")


class Config:
    """Base configuration class for Flask."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

    # Fix the database URL
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('DEBUG', 'True').lower(
    ) == 'true'  # Convert string to boolean


# Print out the final database URI to confirm it's correctly formatted
print(f"✅ DATABASE URI: {Config.SQLALCHEMY_DATABASE_URI}")
 