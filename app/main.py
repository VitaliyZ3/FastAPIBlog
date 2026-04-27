from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.db import AsyncSessionLocal, get_mongo_db
from app.models.article import Article
from app.routers import article, users
import redis.asyncio as redis

REDIS_URL = "redis://localhost:6379"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Set Up test articles
    async with AsyncSessionLocal() as session:
        seed = await session.get(Article, 1)
        if not seed:
            session.add(Article(id=1,name="FastAPI For Beginners", body="some text", user_id=1))
            await session.commit()
    # Create Mongo DB indexed
    database = get_mongo_db()
    await database.get_collection("articles").create_index("name", unique=True, background=True)
    # Redis Set up connection
    app.state.redis = redis.from_url(REDIS_URL, decode_responses=True)
    yield
    await app.state.redis.close()


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(article.router)

