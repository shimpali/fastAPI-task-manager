from typing import List

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_all_tasks() -> List[dict]:
    # Mock response
    tasks = [
        {"id": 1, "title": "Work on a FastAPI project", "status": "in_progress", "due_date": "2023-08-30T10:05:06.944969"},
        {"id": 2, "title": "Write unit tests for FastAPI project", "status": "not_started", "due_date": "2023-08-30T10:05:06.944969"}
    ]

    return tasks
