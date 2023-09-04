import warnings
import os

import pytest
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database

import alembic
from alembic.config import Config


# Apply migrations at beginning and end of testing session
# Set the scope to session so that the db persists for the duration of the testing
# session. Can be removed if fresh DB is needed for each test.
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # Sets the TESTING environment variable to "1", to migrate the testing database instead of the standard db.
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application

    return get_application()


# Grab a reference to the database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    """
    LifespanManager and AsyncClient are used to provide a clean testing client that can send requests to
    the running FastAPI application.
    Ref - https://github.com/florimondmanca/asgi-lifespan
    """
    async with LifespanManager(app):
        async with AsyncClient(
                app=app,
                base_url="http://testserver",
                headers={"Content-Type": "application/json"}
        ) as client:
            yield client
