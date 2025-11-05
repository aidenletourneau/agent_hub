from fastapi import FastAPI
from .api import register_routes
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

register_routes(app)