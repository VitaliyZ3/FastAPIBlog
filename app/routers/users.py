from fastapi import HTTPException, status

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import get_current_user, login_failed_exception
from app.services.jwt import create_access_token
from app.schemas.jwt import TokenCreate

router = APIRouter(prefix="/auth")

@router.get("/users/me")
async def get_current_user(payload: dict = Depends(get_current_user)):
    return payload

@router.post("/create-token")
async def create_jwt(user_data: TokenCreate):
    token = create_access_token(dict(user_data))
    return {"token": token}

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    username = "Vitaliy"
    password = "qwerty"
    if not form_data.password:
        raise login_failed_exception

    # Use db connection to validate user credentials
    if username != form_data.username or password != form_data.password:
        raise login_failed_exception

    data = {"sub": form_data.username, "roles": ["superuser", "admin"]}
    token = create_access_token(data)
    return {"access_token": token}