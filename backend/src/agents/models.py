from pydantic import BaseModel

class CreateAgentRequest(BaseModel):
    name: str
    user_id: str


class GetAgentRequest(BaseModel):
    name: str