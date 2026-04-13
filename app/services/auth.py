from app.services.jwt import (
    create_access_token, decode_token, oauth2_scheme
)
from fastapi import Depends, HTTPException, status

login_failed_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Please, provide correct auth credentials"
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    return payload

def require_role(required_role: str):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        roles = current_user.get("roles", [])
        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return current_user
    return Depends(role_checker)