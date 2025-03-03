from models import Base  # Replace with your actual Base and models
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
import sys
import os

# Add your project's root directory to the Python path
sys.path.append(os.getcwd())

# Import your SQLAlchemy Base and models

# This is the Alembic Config object, which provides access to the values within the .ini file.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add your database URL here
target_metadata = Base.metadata
config.set_main_option(
    'sqlalchemy.url', 'postgresql://user:password@localhost/beauty_shop_ecomm_website')


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
