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
    """
    Retrieve dummy data for testing purposes.

    Returns:
        dict: A dictionary containing the grid dimensions, obstacles, loading stations, and a list of agents.
    """
    data = {
        "length": 10,
        "width": 10,
        "obstacles": "1,3 4,2",
        "loadingStations": "1,1 3,1",
        "agents": [
            {"id": 1, "type": "robot", "positions": ["10,16", "10,15"]},
            {"id": 2, "type": "robot", "positions": ["11,16", "11,15"]},
            {"id": 2, "type": "robot", "positions": ["12,16", "12,15"]},
            {"id": 3, "type": "package", "positions": ["5,6", "5,6"]},
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
