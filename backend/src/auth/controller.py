
from fastapi import APIRouter, Depends, Request
from ..db.core import DbSession

import hashlib
import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qsl, urlencode

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/")
async def test(request: Request, db: DbSession):
    return {"Status": "ok"}
