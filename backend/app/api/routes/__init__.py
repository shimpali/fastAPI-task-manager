from fastapi import APIRouter

from app.api.routes.tasks import router as tasks_router
from app.api.routes.projects import router as projects_router

router = APIRouter()

router.include_router(projects_router, prefix="/projects", tags=["projects"])
router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
