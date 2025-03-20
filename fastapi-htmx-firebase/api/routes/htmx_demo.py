from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Annotated, Union
from fastapi import APIRouter, Form, Request, Header


from uuid import uuid4

class Todo:
    def __init__(self, text: str):
        self.id = uuid4()
        self.text = text
        self.done = False

todos = [Todo("test")]

templates = Jinja2Templates(directory="templates")

htmx_router = APIRouter()

@htmx_router.get("/todo_index", response_class=HTMLResponse)
async def htmx_demo(request: Request):
    return templates.TemplateResponse(request=request, name="todo_index.html")

@htmx_router.get("/todos", response_class=HTMLResponse)
async def list_todos(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@htmx_router.post("/todos", response_class=HTMLResponse)
async def create_todo(request: Request, todo: Annotated[str, Form()]):
    todos.append(Todo(todo))
    return templates.TemplateResponse(
        request=request, name="todos.html", context={"todos": todos}
    )


