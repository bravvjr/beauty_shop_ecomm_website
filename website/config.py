import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")  # Default port for PostgreSQL
    DB_NAME = os.getenv("DB_NAME")

    # Ensure all required variables are set
    required_vars = ["SECRET_KEY", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    # Database URI
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # Logging database connection details (excluding sensitive info)
    logging.info(f"✅ DB_USER: {DB_USER}")
    logging.info(f"✅ DB_HOST: {DB_HOST}")
    logging.info(f"✅ DB_PORT: {DB_PORT}")
    logging.info(f"✅ DB_NAME: {DB_NAME}")

    # Print out the final database URI to confirm it's correctly formatted (excluding password for security)
    masked_password = "******"
    safe_db_uri = f"postgresql://{DB_USER}:{masked_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"✅ DATABASE URI: {safe_db_uri}")

    # MPESA credentials
    MPESA_CONSUMER_KEY = os.getenv("CONSUMER_KEY")  # Corrected variable name
    MPESA_CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")  # Corrected variable name
    MPESA_SHORTCODE = os.getenv("BUSINESS_SHORTCODE")  # Corrected variable name
    MPESA_PASSKEY = os.getenv("PASSKEY")  # Corrected variable name
    MPESA_CALLBACK_URL = os.getenv("CALLBACK_URL")  # Corrected variable name

    # Ensure MPESA variables are set
    mpesa_vars = ["MPESA_CONSUMER_KEY", "MPESA_CONSUMER_SECRET", "MPESA_SHORTCODE", "MPESA_PASSKEY", "MPESA_CALLBACK_URL"]
    missing_mpesa_vars = [var for var in mpesa_vars if not locals()[var]]
    
    if missing_mpesa_vars:
        raise ValueError(f"Missing MPESA environment variables: {', '.join(missing_mpesa_vars)}")

    # Logging MPESA details (excluding sensitive info)
    logging.info(f"✅ MPESA_SHORTCODE: {MPESA_SHORTCODE}")
    logging.info(f"✅ MPESA_CALLBACK_URL: {MPESA_CALLBACK_URL}")
