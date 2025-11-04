from uuid import UUID
from fastapi import HTTPException
from . import models
import logging
from ..db.schemas import User
from ..db.core import DbSession


def get_user_by_id(db: DbSession, user_id: UUID) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logging.warning(f"User not found with ID: {user_id}")
        raise Exception(user_id)
    logging.info(f"Successfully retrieved user with ID: {user_id}")
    return user