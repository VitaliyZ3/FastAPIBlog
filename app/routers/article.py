from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.article import ArticleGet, ArticleCreate, ArticleUpdate
from app.services.db import get_db
from app.models.article import Article
from app.services.redis import get_redis_db, save_articles_cache, get_articles_cached, invalidate_article_cache
from redis.asyncio.client import Redis
import json

router = APIRouter(prefix="/api", tags=["articles"])


@router.get("/article/{id}", response_model=ArticleGet)
async def get_article(id: int, db: AsyncSession = Depends(get_db)):
    article = await db.get(Article, id)
    if not article:
        raise HTTPException(404, "Please, provide correct article id")
    return article


@router.get("/articles/", response_model=list[ArticleGet])
async def search_articles(
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis_db)
):
    articles_cached = await get_articles_cached(redis_client)
    if articles_cached:
        return json.loads(articles_cached)

    query = select(Article)
    articles = (await db.scalars(query)).all()

    await save_articles_cache(articles, redis_client)
    return articles

@router.post("/article/", response_model=ArticleGet, status_code=201)
async def create_article(
        article: ArticleCreate,
        db: AsyncSession = Depends(get_db),
        redis_client: Redis = Depends(get_redis_db)
):
    db_article = Article(**article.model_dump())
    db.add(db_article)
    await db.commit()
    await db.refresh(db_article)
    await invalidate_article_cache(redis_client)
    return db_article


@router.put("/article/{id}", response_model=ArticleGet)
async def update_article(
        id: int,
        article: ArticleUpdate,
        db: AsyncSession = Depends(get_db),
        redis_client: Redis = Depends(get_redis_db)
):
    db_article = await db.get(Article, id)
    if not db_article:
        raise HTTPException(404, "Please, provide correct article id")
    for key, value in article.model_dump().items():
        setattr(db_article, key, value)
    await db.commit()
    await db.refresh(db_article)
    await invalidate_article_cache(redis_client)
    return db_article
