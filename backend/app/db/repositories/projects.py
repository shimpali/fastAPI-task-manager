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