from pydantic import BaseModel

class TokenCreate(BaseModel):
    sub: str