from fastapi import FastAPI
from .db.core import engine, Base
from .api import register_routes


app = FastAPI()


""" Only uncomment below to create new tables, 
otherwise the tests will fail if not connected
"""
# Base.metadata.create_all(bind=engine)

register_routes(app)