import json
import datetime

import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from app.models.project import ProjectCreate

# Decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
def new_project():
    return ProjectCreate(
        title="Project 1",
        description="This is a web app project",
        created_date="2023-09-04T14:08:06.365",
        due_date="2023-11-30T14:08:06.365",
        status="not_started",
    )


class TestProjectsRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("projects:create-project"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("projects:create-project"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateProject:
    async def test_valid_input_creates_project(
            self, app: FastAPI, client: AsyncClient, new_project: ProjectCreate
    ) -> None:
        """
          This test is actually executing queries against a real postgres database. So no mocking needed.
        """
        res = await client.post(
            app.url_path_for("projects:create-project"), json={"new_project": new_project.model_dump_json()}
        )
        assert res.status_code == HTTP_201_CREATED

        created_project = ProjectCreate(**res.json())
        assert created_project == new_project