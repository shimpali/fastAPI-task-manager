from typing import List

from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

from app.models.project import ProjectCreate, ProjectPublic
from app.db.repositories.projects import ProjectsRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.get("/")
async def get_all_projects() -> List[dict]:
    projects = [
        {"id": 1, "title": "Project 1", "description": "This is a web app project",
         "created_date": "2023-09-02T10:05:06.944969", "due_date": "2023-11-30T10:05:06.944969",
         "status": "in_progress"},
        {"id": 2, "title": "Project 2", "description": "This is a mobile app project",
         "created_date": "2023-09-02T10:05:06.944969", "due_date": "2023-12-30T10:05:06.944969",
         "status": "not_started"},
    ]

    return projects


@router.post("/", response_model=ProjectPublic, name="projects:create-project", status_code=HTTP_201_CREATED)
async def create_new_project(
        new_project: ProjectCreate = Body(..., embed=True),
        projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
) -> ProjectPublic:
    created_project = await projects_repo.create_project(new_project=new_project)

    return created_project