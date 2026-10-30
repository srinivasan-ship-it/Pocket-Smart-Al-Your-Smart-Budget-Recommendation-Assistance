from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from app.config import settings

from app.database import init_db

from routes import auth
from routes import planner as planners
from routes import pages


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(

    title=settings.app_name,

    description=(
        "Budget-aware AI recommendations "
        "for Home, Party and Jewelry planning."
    ),

    version="1.0.0",

    lifespan=lifespan
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=settings.cors_list,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.mount(

    "/static",

    StaticFiles(
        directory="static"
    ),

    name="static"
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    planners.router
)


@app.get(
    "/health",
    tags=["System"]
)
def health():

    return {

        "status": "ok",

        "app":
            settings.app_name,

        "ai_configured":
            bool(
                settings.gemini_api_key
                and settings.ai_enabled
            ),

        "model":
            settings.gemini_model
    }


@app.get(
    "/startup",
    tags=["System"]
)
def startup():

    return {

        "status":
            "initialized",

        "message":
            "PocketSmart AI services are ready"
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app.main:app",

        host="127.0.0.1",

        port=8000,

        reload=True
    )