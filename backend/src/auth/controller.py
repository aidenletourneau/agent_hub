from fastapi import APIRouter, Request, Request, Response
from ..db.core import DbSession
from . import service
from . import models
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# STANDARD LOGIN ROUTES
@router.post("/signup")
async def signup(data: models.SignupRequest, request: Request, db: DbSession):
    return service.signup(data, request, db)


@router.post("/login")
async def login(data: models.LoginRequest, request: Request, db: DbSession, response: Response):
    return service.login(data, request, db, response)

@router.post("/docs-login")
async def login(request: Request, db: DbSession, response: Response, form: OAuth2PasswordRequestForm = Depends()):
    data = models.LoginRequest(username=form.username, password=form.password)
    return service.login(data, request, db, response)

# OAUTH ROUTES TODO: MAKE THESE WORK
@router.get("/googleLogin")
def redirect_to_google_oauth():
    return service.redirect_to_google_oauth()


@router.get("/callback")
def auth_callback(request: Request, db: DbSession, code: str | None = None, state: str | None = None):
    return service.google_oauth_callback(request, db, code, state)