from fastapi import APIRouter, Response
from ..db.core import DbSession
from . import service
from . import models
from ..auth.service import CurrentUserId


router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)

# get all agents for a logged in user
@router.get("", response_model=list[models.AgentResponse])
async def get_all_agents(db: DbSession, user: CurrentUserId):
    return service.get_all_agents(db, user)

# create an agent
@router.post("")
async def create_agent(data: models.CreateAgentRequest, db: DbSession, response: Response, user_id: CurrentUserId):
    return service.create_agent(data, db, response, user_id)
    