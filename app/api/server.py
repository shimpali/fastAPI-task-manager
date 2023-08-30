from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router as api_router


def get_application():
    tm_app = FastAPI(title="Task Manager", version="1.0.0")

    tm_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    tm_app.include_router(api_router, prefix="/api")

    return tm_app


app = get_application()
