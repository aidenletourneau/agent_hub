from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e.orig)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error creating DB session: {str(e)}"
        )
    finally:
        db.close()
        
DbSession = Annotated[Session, Depends(get_db)]
