import json
import os

from fastapi import APIRouter, Depends, Request, Request, HTTPException, Response
from fastapi.responses import RedirectResponse, JSONResponse
from ..db.core import DbSession
import bcrypt

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
from dotenv import load_dotenv
from ..db.schemas import User
from sqlalchemy import or_
from pydantic import BaseModel
import jwt
import datetime
load_dotenv()


SCOPES = [
  "https://www.googleapis.com/auth/userinfo.profile",
  "https://www.googleapis.com/auth/userinfo.email",
  "openid"
]

GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
CLIENT_CONFIG = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
        "javascript_origins": ["http://localhost:3000", "http://localhost:8000"],
    }
}


def build_oauth_flow(state: str | None = None) -> Flow:
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        state=state,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )

    flow.code_verifier 
    return flow


def redirect_to_google_oauth():
    flow = build_oauth_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    response = RedirectResponse(auth_url, status_code=302)
    response.set_cookie("oauth_state", state, httponly=True, secure=False, samesite="lax")
    return response

def hash_password(plain: str) -> str:
    salt = bcrypt.gensalt(rounds=12)  # 12–14 is common
    return bcrypt.hashpw(plain.encode(), salt).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


def signup(data: SignupRequest, request: Request, db: DbSession):
    username = data.username
    email = data.email
    password = data.password


    # check if username already in db
    existing_user = db.query(User).filter(or_(User.username == username, User.email == email)).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already taken"
        )
    
    # username and email not taken so create a new user
    # lets hash the password
    hashed_password = hash_password(password)

    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user": {"username": new_user.username, "email": new_user.email}}


class LoginRequest(BaseModel):
    username: str
    password: str


def create_jwt(user: User) -> str:
    payload = {
        "sub": str(user.id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),  # Expiration time
        "iat": datetime.datetime.utcnow(),  # Issued at time
        "iss": "agent-hub",  # Issuer
        "aud": "users"  # Audience
    }
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    encoded_jwt: str = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def login(data: LoginRequest, request: Request, db: DbSession, response: Response):
    username = data.username
    password = data.password

    # lookup user based on username
    user: User = db.query(User).filter(User.username == username).first()
    # no match with username
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No user found with that username"
        ) 

    # verify password
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        ) 

    jwt = create_jwt(user)
    response.set_cookie(
        key="access_token",
        value=jwt,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=15*60,
        path="/",
    )
    response.status_code = 200
    return response


def google_oauth_callback(request: Request, db: DbSession, code: str | None = None, state: str | None = None):
    
    state_cookie = request.cookies.get("oauth_state")
    if not state or not state_cookie or state != state_cookie:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    flow = build_oauth_flow(state=state)
    
    # code for token exchange
    flow.fetch_token(code=code)

    creds = flow.credentials
    id_token_value = creds.id_token 

    idinfo = id_token.verify_oauth2_token(
        id_token_value,
        GoogleRequest(),           # this is for internal google oauth use
        os.getenv("GOOGLE_CLIENT_ID")           
    )

    # create a new user
    user = User(
        google_sub=idinfo["sub"],
        email=idinfo.get("email"),
        image_url=idinfo.get("picture"),
        username=idinfo.get("email")
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # create jwt
    jwt = create_jwt(user)

    response = Response
    return {"jwt": jwt}

