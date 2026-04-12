from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from todo.routers import auth, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>Todo - FastAPI</title>
        </head>
        <body style="background-color: #fcfcfc;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #5c5c5c">
            <div>
                <p style="font: bold 32px/1.5 'Arial', sans-serif;
                text-align: center; color: #050505">
                    TODO
                </p>
                <p style="font: bold 24px/1.5 'Arial', sans-serif;">
                    Hello - API FastAPI
                </p>
            </div>
        </body>
    </html>
"""
