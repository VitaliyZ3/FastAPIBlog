from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.article import ArticleGet, ArticleCreate, ArticleUpdate
from app.services.db import get_db, get_mongo_db
from app.models.article import Article
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

router = APIRouter(prefix="/api", tags=["articles"])


@router.get("/article/{id}", response_model=ArticleGet)
async def get_article(id: int, db: AsyncSession = Depends(get_db)):
    article = await db.get(Article, id)
    if not article:
        raise HTTPException(404, "Please, provide correct article id")
    return article


@router.get("/articles/", response_model=list[ArticleGet])
async def search_articles(
    name: str | None = None,
    limit: int = Query(10, gt=0, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Article).limit(limit)
    if name:
        query = query.where(Article.name.ilike(f"%{name}%"))
    result = await db.execute(query)
    return result.scalars().all()

#
# @router.post("/article/", response_model=ArticleGet, status_code=201)
# async def create_article(article: ArticleCreate, db: AsyncSession = Depends(get_db)):
#     db_article = Article(**article.model_dump())
#     db.add(db_article)
#     await db.commit()
#     await db.refresh(db_article)
#     return db_article


@router.post("/article/", response_model=ArticleGet, status_code=201)
async def create_article(article: ArticleCreate, db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    article = {
        "_id": ObjectId(),
        **article.model_dump()
    }
    collection = db.get_collection("articles")
    await collection.insert_one(article)
    return article


@router.put("/article/{id}", response_model=ArticleGet)
async def update_article(id: int, article: ArticleUpdate, db: AsyncSession = Depends(get_db)):
    db_article = await db.get(Article, id)
    if not db_article:
        raise HTTPException(404, "Please, provide correct article id")
    for key, value in article.model_dump().items():
        setattr(db_article, key, value)
    await db.commit()
    await db.refresh(db_article)
    return db_article
