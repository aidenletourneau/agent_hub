from fastapi import FastAPI
from .auth.controller import router as auth_router
from .agents.controller import router as agent_router
from .users.controller import router as user_router


def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(agent_router)
    app.include_router(user_router)

