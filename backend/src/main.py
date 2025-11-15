from fastapi import FastAPI
from .api import register_routes
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
load_dotenv()

# Define allowed origins
origins = [
    os.getenv("LOCAL_FRONTEND_URL"),   # your Next.js dev server
    'http://localhost:5173'
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # List of allowed origins
    allow_credentials=True,           # Allow cookies, Authorization headers
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers (Content-Type, Authorization, etc.)
)

register_routes(app)