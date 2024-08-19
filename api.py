from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Mesa API"
    APP_VERSION: str = "1.0.0"
    ALLOWED_HOSTS: list[str] = ["*"]
    API_KEY: str = "secret-key"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings():
    return Settings()  # type: ignore


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()


@api_router.get("/healthy")
def health() -> str:
    return "healthy"


@api_router.get("/dummy")
def dummy() -> dict:
    data = {
        "length": 10,
        "width": 10,
        "obstacles": "1,3 4,2",
        "loadingStation": "1,1 3,1",
        "steps": [
            {
                "step": 1,
                "agents": [
                    {"id": 1, "type": "robot", "pos": "1,2"},
                    {"id": 2, "type": "robot", "pos": "1,4"},
                    {"id": 1, "type": "packages", "pos": "1,6"},
                ],
            },
            {
                "step": 2,
                "agents": [
                    {"id": 1, "type": "robot", "pos": "2,2"},
                    {"id": 2, "type": "robot", "pos": "2,4"},
                    {"id": 1, "type": "packages", "pos": "1,6"},
                ],
            },
        ],
    }
    return data


def get_api() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="An interface to our Mesa models",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(api_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    return app
