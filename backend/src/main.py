from fastapi import FastAPI
from .api import register_routes
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()


""" Only uncomment below to create new tables, 
otherwise the tests will fail if not connected
"""
# Base.metadata.create_all(bind=engine)

register_routes(app)