from pydantic import BaseModel, Field, field_validator
from pydantic import ConfigDict
from typing import Optional


class BaseArticle(BaseModel):
    name: str = Field(min_length=10, max_length=258)
    body: str | None = None
    user_id: int = Field(gt=0)


class ArticleGet(BaseArticle):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ArticleCreate(BaseArticle):
    name: str = Field(min_length=10, max_length=258, description="Note, that 'Django' can`t be in article name")

    @field_validator("name")
    @classmethod
    def validate_name_not_django(cls, value: str) -> str:
        if "django" in value.lower():
            raise ValueError("Django can`t be in article name")
        return value


class ArticleUpdate(BaseArticle):
    pass
