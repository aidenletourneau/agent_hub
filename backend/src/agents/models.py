from pydantic import BaseModel
from uuid import UUID
class CreateAgentRequest(BaseModel):
    name: str

class GetAgentRequest(BaseModel):
    name: str

class AgentResponse(BaseModel):
    id:  UUID
    name:  str
    