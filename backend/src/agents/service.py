from fastapi import Response
from ..db.core import DbSession
from ..db.schemas import User, Agent
from dotenv import load_dotenv
from . import models
from ..auth.service import CurrentUserId
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_all_agents(db: DbSession, user: CurrentUserId):
    try:
        agents = db.query(Agent).filter(Agent.user_id == user).all()
        return agents
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Error fetching user agents"
        )
    

def create_agent(data: models.CreateAgentRequest, db: DbSession, response: Response, user: CurrentUserId):
    # check if username already in db
    existing_agent = db.query(Agent).filter(Agent.name == data.name, Agent.user_id == user.user_id).first()
    if existing_agent:
        raise HTTPException(
            status_code=400,
            detail="agent name already taken"
        )
    
    new_agent = Agent(name=data.name, user_id=user.user_id)
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    response.status_code = 201
    return response