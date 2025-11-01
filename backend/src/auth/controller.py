import os

from fastapi import APIRouter, Depends, Request, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from ..db.core import DbSession

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
  "https://www.googleapis.com/auth/userinfo.profile",
  "https://www.googleapis.com/auth/userinfo.email",
  "openid"
]

# for convienience
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


def build_flow(state: str | None = None) -> Flow:
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        state=state,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI"),
    )

    flow.code_verifier 
    return flow

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/")
async def test(request: Request, db: DbSession):
    return {"Status": "ok"}

@router.get("/login")
def auth_login():
    flow = build_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",            # to receive refresh_token (first consent)
        include_granted_scopes="true",    # incremental auth
        prompt="consent",                 # force consent page (ensures refresh_token first time)
    )

    response = RedirectResponse(auth_url, status_code=302)
    response.set_cookie("oauth_state", state, httponly=True, secure=False, samesite="lax")
    return response


@router.get("/callback")
def auth_callback(request: Request, code: str | None = None, state: str | None = None):
    
    state_cookie = request.cookies.get("oauth_state")
    if not state or not state_cookie or state != state_cookie:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    flow = build_flow(state=state)
    
    # code for token exchange
    flow.fetch_token(code=code)

    creds = flow.credentials
    id_token_value = creds.id_token 

    idinfo = id_token.verify_oauth2_token(
        id_token_value,
        GoogleRequest(),           # this is for internal google oauth use
        os.getenv("GOOGLE_CLIENT_ID")           
    )

    user = {
        "sub": idinfo["sub"],
        "email": idinfo.get("email"),
        "email_verified": idinfo.get("email_verified", False),
        "name": idinfo.get("name"),
        "picture": idinfo.get("picture"),
    }

    # OPTIONAL: persist creds.refresh_token and creds.token (access token) server-side
    # save_tokens_to_db(user["sub"], creds.refresh_token, creds.token, creds.expiry)

    # Issue your own app session (e.g., JWT or cookie)
    # For demo return the user payload:
    return JSONResponse({"user": user})
    