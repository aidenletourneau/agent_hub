import json
import os
from typing import Annotated

from fastapi import Depends, Request, Request, HTTPException, Response, status
from fastapi.responses import RedirectResponse, JSONResponse
from ..db.core import DbSession
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
from dotenv import load_dotenv
from ..db.schemas import User
from sqlalchemy import or_
import jwt
import datetime
from . import models


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
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
        "javascript_origins": os.getenv("GOOGLE_JAVASCRIPT_ORIGINS").split(','),
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


def signup(data: models.SignupRequest, request: Request, db: DbSession):
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



def login(data: models.LoginRequest, request: Request, db: DbSession, response: Response):
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

    userDict = user.to_safe_json()
    return {"user": userDict}


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

    # check if user exists
    user: User = db.query(User).filter(User.google_sub == idinfo["sub"]).first()
    
    if not user:
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

    FRONTEND_URL = os.getenv("LOCAL_FRONTEND_URL")
    # redirect to homepage
    response = RedirectResponse(f"{FRONTEND_URL}", status_code=302)
    response.set_cookie(
        key="access_token",
        value=jwt,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=15*60,
        path="/",
    )
    return response




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/docs-login")
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
CurrentToken = Annotated[str, Depends(oauth2_scheme)]

def verify_token(token: str) -> models.TokenData:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], audience="users", issuer="agent-hub")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: no sub")
        
        return models.TokenData(user_id=user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )



def get_current_user(token: CurrentToken, db: DbSession) -> models.TokenData:
    return verify_token(token)

CurrentUser = Annotated[models.TokenData, Depends(get_current_user)]


def logout(request: Request, response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"
    )
    return {"detail": "logged out"}