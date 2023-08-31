from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import config, core_tasks

from app.api.routes import router as api_router


def get_application():
    tm_app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    tm_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    tm_app.add_event_handler("startup", core_tasks.create_start_app_handler(tm_app))
    tm_app.add_event_handler("shutdown", core_tasks.create_stop_app_handler(tm_app))

    tm_app.include_router(api_router, prefix="/api")

    return tm_app


app = get_application()