from pydantic import (
    BaseModel, Field, EmailStr,
    field_validator
)
from typing import Optional

class BaseArticle(BaseModel):
    name: str = Field(min_length=10, max_length=258)
    body: str | None = None
    user_id: int = Field(gt=0)

class ArticleGet(BaseArticle):
    pass

class ArticleCreate(BaseArticle):
    id: int = Field(gt=0)
    name: str = Field(description="Note, that 'Django' can`t be in article name")

    @field_validator("name")
    @classmethod
    def validate_name_not_django(cls, value: str) -> str:
        if "django" in value.lower():
            raise ValueError("Django can`t be in article name")
        else:
            return value

class ArticleUpdate(BaseArticle):
    pass

