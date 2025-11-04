from typing import Annotated
from fastapi import APIRouter, Depends, Request, Request, Response, status
from pydantic import BaseModel
from ..db.core import DbSession
from ..db.schemas import User, Agent
from dotenv import load_dotenv
from . import service
from . import models
from fastapi import HTTPException
from ..auth.service import CurrentUser

from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=models.UserResponse)
def get_current_user(current_user: CurrentUser, db: DbSession):
    return service.get_user_by_id(db, current_user.get_uuid())