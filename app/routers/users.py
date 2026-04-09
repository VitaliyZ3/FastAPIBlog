from fastapi import APIRouter

router = APIRouter(prefix="/auth")

@router.get("/users/{id}")
async def get_user(id: int):
    user = {
        "id": id,
        "username": "Oleh",
        "email": "oleh@gmail.com"
    }
    return user