import pathlib
import sys
import os

import alembic
from sqlalchemy import engine_from_config, create_engine, pool
from psycopg2 import DatabaseError

from logging.config import fileConfig
import logging

# we're appending the app directory to our path here so that we can import config easily
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import DATABASE_URL, POSTGRES_DB  # noqaß

# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode
    """
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else str(DATABASE_URL)

    # Handle testing config for migrations
    if os.environ.get("TESTING"):
        # Connect to primary db - postgres_test Specify the "AUTOCOMMIT" option for isolation_level to avoid manual
        # transaction management when creating databases.
        # Sqlalchemy always tries to run queries in a transaction,
        # and postgres does not allow users to create databases inside a transaction.
        # To get around that, end each open transaction automatically after execution.
        # That allows to drop a database and then create a new one inside the default connection.
        default_engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")
        # Drop TESTING db if it exists and create a fresh one
        with default_engine.connect() as default_conn:
            default_conn.execute(f'DROP DATABASE IF EXISTS {POSTGRES_DB}_test')
            default_conn.execute(f'CREATE DATABASE {POSTGRES_DB}_test')

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", DB_URL)

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(
            connection=connection,
            target_metadata=None
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    if os.environ.get("TESTING"):
        raise DatabaseError("Running testing migrations offline currently not permitted.")

    alembic.context.configure(url=str(DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
