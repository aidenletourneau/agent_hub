from sqlalchemy import create_engine
from src.db.schemas import Base
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# This creates tables that don't exist yet
print("Creating missing tables...")
Base.metadata.create_all(engine)
print("Tables are up to date!")
