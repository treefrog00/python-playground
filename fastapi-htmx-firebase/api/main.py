# firebase auth based on https://github.com/adamcohenhillel/simple_fastapi_with_firebase
# htmx based on https://testdriven.io/blog/fastapi-htmx/

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.routing import APIRouter

from api.routes.firebase_routes import firebase_router
from api.routes.htmx_demo import htmx_router
from api.lifetime import register_shutdown_event, register_startup_event
from api.exception_handlers import register_exception_handlers

def get_app() -> FastAPI:
    app = FastAPI(
        title='Template App',
        description='This is Template',
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        openapi_url='/api/openapi.json',
        default_response_class=UJSONResponse,
    )

    register_startup_event(app)
    register_shutdown_event(app)
    register_exception_handlers(app)

    # api_router = APIRouter()
    app.include_router(router=firebase_router, prefix='/firebase')
    app.include_router(router=htmx_router, prefix='/htmx', tags=['htmx'])

    return app

app = get_app()