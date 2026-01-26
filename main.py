import uvicorn
import threading
from fastapi import FastAPI
from src.routes.users_router import router as users_router


app = FastAPI()

app.include_router(users_router)


def create_server(port=8000):
    config = uvicorn.Config(app=app, port=port)
    server = uvicorn.Server(config=config)
    return server


if __name__ == '__main__':
    server = create_server()
    server.run()
