from typing import List

import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from app.models.project import ProjectCreate, ProjectInDB

# Decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
def new_project():
    return ProjectCreate(
        title='Project 1',
        description='This is a web app project',
        created_date='2023-09-04T14:08:06.365',
        due_date='2023-11-30T14:08:06.365',
        status='not_started',
    )


class TestProjectsRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for('projects:create-project'), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for('projects:create-project'), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateProject:
    async def test_valid_input_creates_project(
            self, app: FastAPI, client: AsyncClient, new_project: ProjectCreate
    ) -> None:
        '''
          This test is actually executing queries against a real postgres database. So no mocking needed.
        '''
        project = {'title': 'Project 1', 'description': 'This is a web app project',
         'created_date': '2023-09-02T10:05:06.944969', 'due_date': '2023-11-30T10:05:06.944969',
         'status': 'in_progress'}
        res = await client.post( # TODO: Fix the below
            # app.url_path_for('projects:create-project'), json={'new_project': new_project.model_dump_json()}
            app.url_path_for('projects:create-project'), json={'new_project': project}
        )
        assert res.status_code == HTTP_201_CREATED

        # created_project = ProjectCreate(**res.json())
        # assert created_project == new_project
        created_project = res.json()
        assert created_project['id'] == 1

        @pytest.mark.parametrize(
            'invalid_payload, status_code',
            (
                    (None, 422),
                    ({}, 422),
                    ({'title': 'test_title'}, 422),
                    ({'created_date': '2023-10-10'}, 422),
                    ({'title': 'test_title', 'description': 'test'}, 422),
            ),
        )
        async def test_invalid_input_raises_error(
                self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int
        ) -> None:
            res = await client.post(
                app.url_path_for('projects:create-project'), json={'new_project': invalid_payload}
            )
            assert res.status_code == status_code


class TestGetProject:
    async def test_get_project_by_id(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for('projects:get-project-by-id', id=1))
        assert res.status_code == HTTP_200_OK
        project = ProjectInDB(**res.json())
        assert project.id == 1

    async def test_get_project_by_id_with_fixture(self, app: FastAPI, client: AsyncClient, test_project: ProjectInDB) -> None:
        res = await client.get(app.url_path_for('projects:get-project-by-id', id=test_project.id))
        assert res.status_code == HTTP_200_OK
        project = ProjectInDB(**res.json())
        assert project == test_project

    @pytest.mark.parametrize(
        'id, status_code',
        (
                (500, 404),
                (-1, 404),
                (None, 422),
        ),
    )
    async def test_wrong_id_returns_error(
            self, app: FastAPI, client: AsyncClient, id: int, status_code: int
    ) -> None:
        res = await client.get(app.url_path_for('projects:get-project-by-id', id=id))
        assert res.status_code == status_code
        
    async def test_get_all_projects_returns_valid_response(  
        self, app: FastAPI, client: AsyncClient, test_project: ProjectInDB  
    ) -> None:  
        res = await client.get(app.url_path_for('projects:get-all-projects'))  
        assert res.status_code == HTTP_200_OK  
        assert isinstance(res.json(), list)  
        assert len(res.json()) > 0  
        projects = [ProjectInDB(**l) for l in res.json()]  
        assert test_project in projects


class TestUpdateProject:
    @pytest.mark.parametrize(
        'attrs_to_change, values',
        (
                (['title'], ['new fake project']),
                (['description'], ['new fake project description']),
                (['created_date'], ['2023-09-02T10:05:06.944969']),
                (['due_date'], ['2023-12-02T10:05:06.944969']),
                (['status'], ['not_started']),
                (
                        ['title', 'description'],
                        [
                            'extra new fake project title',
                            'extra new fake project description',
                        ],
                ),
                (['created_date', 'status'], ['2023-09-02T10:05:06.944969', 'in_progress']),
        ),
    )
    async def test_update_project_with_valid_input(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_project: ProjectInDB,
            attrs_to_change: List[str],
            values: List[str],
    ) -> None:
        project_update = {
            'project_update': {
                attrs_to_change[i]: values[i] for i in range(len(attrs_to_change))
            }
        }

        res = await client.put(
            app.url_path_for(
                'projects:update-project-by-id',
                id=test_project.id,
            ),
            json=project_update
        )
        assert res.status_code == HTTP_200_OK
        updated_project = ProjectInDB(**res.json())
        assert updated_project.id == test_project.id  # Make sure it's the same project
        # Make sure that any updated attribute has changed to the correct value
        for i in range(len(attrs_to_change)):
            attr_to_change = getattr(updated_project, attrs_to_change[i])
            assert attr_to_change != getattr(test_project, attrs_to_change[i])
            assert attr_to_change == values[i]
        # Make sure that no other attributes' values have changed
        for attr, value in updated_project.model_dump().items():
            if attr not in attrs_to_change:
                assert getattr(test_project, attr) == value

    @pytest.mark.parametrize(
        'id, payload, status_code',
        (
                (-1, {'title': 'test'}, 422),
                (0, {'title': 'test2'}, 422),
                (500, {'title': 'test3'}, 404),
                (1, None, 422),
                (1, {'status': 'invalid project type'}, 422),
                (1, {'status': None}, 400),
        ),
    )
    async def test_update_project_with_invalid_input_throws_error(
            self,
            app: FastAPI,
            client: AsyncClient,
            id: int,
            payload: dict,
            status_code: int,
    ) -> None:
        project_update = {'project_update': payload}

        res = await client.put(
            app.url_path_for('projects:update-project-by-id', id=id),
            json=project_update
        )
        assert res.status_code == status_code


class TestDeleteProject:
    async def test_can_delete_project_successfully(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_project: ProjectInDB,
    ) -> None:
        # delete the project
        res = await client.delete(
            app.url_path_for(
                "projects:delete-project-by-id",
                id=test_project.id,
            ),
        )
        assert res.status_code == HTTP_200_OK
        # ensure that the project no longer exists
        res = await client.get(
            app.url_path_for(
                "projects:get-project-by-id",
                id=test_project.id,
            ),
        )
        assert res.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "id, status_code",
        (
                (500, 404),
                (0, 422),
                (-1, 422),
                (None, 422),
        ),
    )
    async def test_delete_project_with_invalid_input_throws_error(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_project: ProjectInDB,
            id: int,
            status_code: int,
    ) -> None:
        res = await client.delete(
            app.url_path_for("projects:delete-project-by-id", id=id),
        )
        assert res.status_code == status_code