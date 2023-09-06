from typing import List

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories.base import BaseRepository
from app.models.project import ProjectCreate, ProjectUpdate, ProjectInDB

CREATE_PROJECT_QUERY = """
    INSERT INTO projects (title, description, created_date, due_date, status)
    VALUES (:title, :description, :created_date, :due_date, :status)
    RETURNING id, title, description, created_date, due_date, status;
"""

GET_PROJECT_BY_ID_QUERY = """
    SELECT id, title, description, created_date, due_date, status
    FROM projects
    WHERE id = :id;
"""

GET_ALL_PROJECTS_QUERY = """
    SELECT id, title, description, created_date, due_date, status
    FROM projects;
"""

UPDATE_PROJECT_BY_ID_QUERY = """
    UPDATE projects  
    SET title        = :title,  
        description  = :description,  
        due_date     = :due_date,  
        status       = :status  
    WHERE id = :id  
    RETURNING id, title, description, created_date, due_date, status;  
"""

DELETE_PROJECT_BY_ID_QUERY = """
    DELETE FROM projects 
    WHERE id = :id 
    RETURNING id;
"""


class ProjectsRepository(BaseRepository):
    """"
    All database actions associated with the Project resource
    """

    async def create_project(self, *, new_project: ProjectCreate) -> ProjectInDB:
        query_values = new_project.model_dump()
        project = await self.db.fetch_one(query=CREATE_PROJECT_QUERY, values=query_values)

        return ProjectInDB(**project)

    async def get_project_by_id(self, *, id: int) -> ProjectInDB:
        project = await self.db.fetch_one(query=GET_PROJECT_BY_ID_QUERY, values={"id": id})

        if not project:
            return None

        return ProjectInDB(**project)

    async def get_all_projects(self) -> List[ProjectInDB]:
        project_records = await self.db.fetch_all(
            query=GET_ALL_PROJECTS_QUERY,
        )

        return [ProjectInDB(**project) for project in project_records]

    async def update_project(
            self, *, id: int, project_update: ProjectUpdate,
    ) -> ProjectInDB:
        project = await self.get_project_by_id(id=id)

        if not project:
            return None

        project_update_params = project.copy(
            update=project_update.dict(exclude_unset=True, exclude_none=True),
        )
        
        if project_update_params.status is None:
            raise HTTPException(  
                status_code=HTTP_400_BAD_REQUEST,  
                detail="Invalid project status. Cannot be None.",
            )  

        try:
            updated_project = await self.db.fetch_one(
                query=UPDATE_PROJECT_BY_ID_QUERY,
                values=project_update_params.dict(),
            )
            return ProjectInDB(**updated_project)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid update params.",
            )

    async def delete_project_by_id(self, *, id: int) -> int:
        project = await self.get_project_by_id(id=id)

        if not project:
            return None

        deleted_id = await self.db.execute(
            query=DELETE_PROJECT_BY_ID_QUERY,
            values={"id": id},
        )

        return deleted_id