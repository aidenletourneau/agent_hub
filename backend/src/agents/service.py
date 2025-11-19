from fastapi import Response
from ..db.core import DbSession
from ..db.schemas import User, Agent
from . import models
from ..auth.service import CurrentUserId
from fastapi import HTTPException
from . import models


def get_all_agents(db: DbSession, user: CurrentUserId) -> list[models.AgentResponse]:
    try:
        agents = db.query(Agent).filter(Agent.user_id == user).all()
        return agents
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Error fetching user agents"
        )

def create_agent(data: models.CreateAgentRequest, db: DbSession, response: Response, user_id: CurrentUserId):

    # check if agent already in db for this user
    existing_agent = db.query(Agent).filter(Agent.name == data.name, Agent.user_id == user_id).first()
    if existing_agent:
        raise HTTPException(
            status_code=400,
            detail="agent name already taken"
        )
    
    new_agent = Agent(
        user_id=user_id, 
        name=data.name, 
        description=data.description
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    response.status_code = 201
    return response