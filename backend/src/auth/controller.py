from fastapi import APIRouter, Request, Request, Response

from ..db.schemas import User
from ..db.core import DbSession
from . import service
from . import models
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# GET THE CURRENT USER BASED ON ACCESS TOKEN
@router.get("/me")
async def get_current_user(request: Request, db: DbSession, response: Response):
    access_token = request.cookies.get("access_token")

    token_data: models.TokenData = service.verify_token(access_token)
    user_id = token_data.user_id

    user: User = db.query(User).filter(User.id == user_id).first()

    if not user:
        pass

    response.status_code = 200
    safe_user_json = user.to_safe_json()
    return {"user": safe_user_json}




# STANDARD LOGIN ROUTES
@router.post("/signup")
async def signup(data: models.SignupRequest, request: Request, db: DbSession):
    return service.signup(data, request, db)

@router.post("/login")
async def login(data: models.LoginRequest, request: Request, db: DbSession, response: Response):
    return service.login(data, request, db, response)

@router.post("/logout")
async def login(request: Request, response: Response):
    return service.logout(request, response)

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