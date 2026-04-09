from fastapi import APIRouter, Query, HTTPException
from app.schemas.article import ArticleGet, ArticleCreate, ArticleUpdate
from app.schemas.base_schema import PutResponseMessage
from app.services.db import get_articles

router = APIRouter(prefix="/api", tags=["articles"])


@router.get("/article/{id}", response_model=ArticleGet)
async def get_article(id: int):
    articles = await get_articles()
    if id not in articles:
        raise HTTPException(404, "Please, provide correct article id")
    return articles[id]

@router.get("/articles/", response_model=list[ArticleGet])
async def search_articles(
    name: str | None = None,
    limit: int = Query(10, gt=0, le=100),
):
    articles = await get_articles()
    return articles.values()

@router.post("/article/", response_model=ArticleGet, status_code=201)
async def create_article(article: ArticleCreate):
    articles = await get_articles()
    if article.id in articles:
        raise HTTPException(422, "You cant create article with existing id")
    articles[article.id] = article
    return article

@router.put("/article/{id}", response_model=ArticleGet)
async def update_article(id: int, article: ArticleUpdate):
    articles = await get_articles()
    if id not in articles:
        raise HTTPException(404, "Please, provide correct article id")
    articles[id] = article
    return article

@router.delete("/article/{id}")
async def delete_article(article_id: int):
    articles = await get_articles()
    if not article_id in articles:
        raise HTTPException(404, "Please, provide correct article id")
    articles.pop(article_id)
    return {"message": "Deleted"}