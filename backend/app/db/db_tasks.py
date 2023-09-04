import os
from fastapi import FastAPI
from databases import Database
from app.core.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    # if TESTING, Turn postgres into postgres_test
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else DATABASE_URL
    database = Database(DB_URL, min_size=2, max_size=10) # these can be configured in config as well

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    """
    When the app shuts down, disconnect from the database to clean things up
    """
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")