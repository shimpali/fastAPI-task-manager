from typing import List, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.project import ProjectCreate, ProjectPublic, ProjectUpdate
from app.db.repositories.projects import ProjectsRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.get("/", response_model=List[ProjectPublic], name="projects:get-all-projects")
async def get_all_projects(projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository))) -> List[
    dict]:
    """
    :param projects_repo: The DB interface
    :return: List of all projects
    """
    # projects = [
    #     {"id": 1, "title": "Project 1", "description": "This is a web app project",
    #      "created_date": "2023-09-02T10:05:06.944969", "due_date": "2023-11-30T10:05:06.944969",
    #      "status": "in_progress"},
    #     {"id": 2, "title": "Project 2", "description": "This is a mobile app project",
    #      "created_date": "2023-09-02T10:05:06.944969", "due_date": "2023-12-30T10:05:06.944969",
    #      "status": "not_started"},
    # ]

    return await projects_repo.get_all_projects()


@router.post("/", response_model=ProjectPublic, name="projects:create-project", status_code=HTTP_201_CREATED)
async def create_new_project(
        new_project: ProjectCreate = Body(..., embed=True),
        projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
) -> ProjectPublic:
    """
    :param new_project: If you want it to expect a JSON with a key new_project and inside of it the model contents, as it does when you declare extra body parameters, you can use the special Body parameter embed

    :param projects_repo: The DB interface

    :return: FastAPI automatically validates and converts the created_project to an instance of ProjectPublic model, and sends the appropriate JSON as a response.
    """
    created_project = await projects_repo.create_project(new_project=new_project)

    return created_project


@router.get("/{id}/", response_model=ProjectPublic, name="projects:get-project-by-id")
async def get_project_by_id(
        id: int, projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository))
) -> ProjectPublic:
    project = await projects_repo.get_project_by_id(id=id)

    if not project:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No project found with that id.")

    return project


@router.put(
    "/{id}/",
    response_model=ProjectPublic,
    name="projects:update-project-by-id",
)
async def update_project_by_id(
        id: int = Path(..., ge=1, title="The ID of the project to update."),
        project_update: ProjectUpdate = Body(..., embed=True),
        projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
) -> ProjectPublic:
    updated_project = await projects_repo.update_project(
        id=id, project_update=project_update,
    )

    if not updated_project:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No project found with that id.",
        )

    return updated_project


@router.delete("/{id}/", response_model=int, name="projects:delete-project-by-id")
async def delete_project_by_id(
        id: int = Path(..., ge=1, title="The ID of the project to delete."),
        projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
) -> int:
    deleted_id = await projects_repo.delete_project_by_id(id=id)

    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No project found with that id.",
        )

    return deleted_id
