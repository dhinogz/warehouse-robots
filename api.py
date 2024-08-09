from fastapi import FastAPI, APIRouter

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from model import RobotModel


def get_api() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """

    app = FastAPI(
        title="Mesa API",
        version="0.0.1",
        description="An interface to our Mesa models",
        openapi_url="/openapi.json",
        docs_url="/",
    )
    app.include_router(api_router)

    # Sets all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


api_router = APIRouter()


@api_router.get("/mesa")
def get_mesa() -> str:
    res = ""
    positions = [(0, 8), (9, 1)]
    m = RobotModel(10, 10, positions)
    res += f"before{m.robot_positions}  "
    m.step()
    res += f"after{m.robot_positions}"

    return res
