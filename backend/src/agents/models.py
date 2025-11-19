from pydantic import BaseModel
from uuid import UUID
class CreateAgentRequest(BaseModel):
    name: str
    description: str

class GetAgentRequest(BaseModel):
    name: str

class AgentResponse(BaseModel):
    id:  UUID
    name:  str
    protocolVersion: str
    description: str
    url: str
    version: str