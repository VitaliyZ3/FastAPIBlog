from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.services.db import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(258), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
