from fastapi import APIRouter, Request, Request, Response
from ..db.core import DbSession
from dotenv import load_dotenv
from . import service
from . import model
load_dotenv()


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# STANDARD LOGIN ROUTES
@router.post("/signup")
async def signup(data: model.SignupRequest, request: Request, db: DbSession):
    return service.signup(data, request, db)


@router.post("/login")
async def login(data: model.LoginRequest, request: Request, db: DbSession, response: Response):
    return service.login(data, request, db, response)


# OAUTH ROUTES
@router.get("/googleLogin")
def redirect_to_google_oauth():
    return service.redirect_to_google_oauth()


@router.get("/callback")
def auth_callback(request: Request, db: DbSession, code: str | None = None, state: str | None = None):
    return service.google_oauth_callback(request, db, code, state)