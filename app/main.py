from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.db import engine, Base, AsyncSessionLocal
from app.models.article import Article
from app.routers import article, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        seed = await session.get(Article, 1)
        if not seed:
            session.add(Article(id=1, name="FastAPI For Beginners", body="some text", user_id=1))
            await session.commit()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(article.router)
