# firebase auth based on https://github.com/adamcohenhillel/simple_fastapi_with_firebase
# htmx based on https://testdriven.io/blog/fastapi-htmx/

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.routing import APIRouter

from api.routes.firebase_routes import firebase_router
from api.routes.htmx_demo import htmx_router
from api.exception_handlers import register_exception_handlers

import firebase_admin
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize firebase using application default credentials
    firebase_admin.initialize_app()
    yield
    # no shutdown needed

def get_app() -> FastAPI:
    app = FastAPI(
        title='Template App',
        description='This is Template',
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        openapi_url='/api/openapi.json',
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )

    register_exception_handlers(app)

    app.include_router(router=firebase_router, prefix='/firebase')
    app.include_router(router=htmx_router, prefix='/htmx', tags=['htmx'])

    return app

app = get_app()