from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.db import AsyncSessionLocal, get_mongo_db
from app.models.article import Article
from app.routers import article, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as session:
        seed = await session.get(Article, 1)
        if not seed:
            session.add(Article(id=1,name="FastAPI For Beginners", body="some text", user_id=1))
            await session.commit()

    database = get_mongo_db()
    await database.get_collection("articles").create_index("name", unique=True, background=True)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(article.router)

{
    "name": "sadas",
    "body": "sdad",
}