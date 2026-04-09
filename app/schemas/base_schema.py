from pydantic import BaseModel

class PutResponseMessage(BaseModel):
    message: str
    data: dict