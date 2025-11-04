from fastapi import APIRouter, Depends, Request, Request, Response
from ..db.core import DbSession
from ..db.schemas import User, Agent
from dotenv import load_dotenv
from . import service
from . import models
from ..auth.service import CurrentUser
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)


async def get_agent( request: Request, db: DbSession, user: CurrentUser, name: str | None = None):
    # TODO: get all users agents with a service function
    return {"user": user.username}


@router.post("/")
async def create_agent(data: models.CreateAgentRequest, request: Request, db: DbSession, response: Response):
    # check if username already in db
    existing_agent = db.query(Agent).filter(Agent.name == data.name).first()
    if existing_agent:
        raise HTTPException(
            status_code=400,
            detail="agent name already taken"
        )
    
    new_agent = Agent(name=data.name, user_id=data.user_id)
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    response.status_code = 201
    return response
    