from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from todo.routers import auth, todos, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>Todo - FastAPI</title>
        </head>
        <body style="background-color: #0c0c0c;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #5c5c5c">
            <div>
                <p style="font: bold 24px/1.5 'Arial', sans-serif;">
                    Hello - API FastAPI
                </p>
            </div>
        </body>
    </html>
"""
