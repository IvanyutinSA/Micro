import uvicorn
from fastapi import FastAPI
from src.routes.users_router import router as users_router
from src.exceptions.middleware import ExceptionMiddleware


app = FastAPI(root_path="/users",
              servers=[{"url": "/users"}])

app.include_router(users_router)
app.add_middleware(ExceptionMiddleware)


def create_server(port=8000):
    config = uvicorn.Config(app=app, port=port, host='0.0.0.0')
    server = uvicorn.Server(config=config)
    return server


if __name__ == '__main__':
    server = create_server()
    server.run()
