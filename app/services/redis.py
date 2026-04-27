from fastapi.requests import Request
from redis.asyncio.client import Redis
from fastapi.encoders import jsonable_encoder
import json

ARTICLES_CACHE_KEY = "all_articles"

def get_redis_db(request: Request):
    return request.app.state.redis

async def save_articles_cache(articles: dict, redis_client: Redis):
    articles_list = jsonable_encoder(articles)
    articles_json = json.dumps(articles_list)
    await redis_client.set(ARTICLES_CACHE_KEY, articles_json)

async def get_articles_cached(redis_client: Redis):
    return await redis_client.get(ARTICLES_CACHE_KEY)

async def invalidate_article_cache(redis_client: Redis):
    await redis_client.delete(ARTICLES_CACHE_KEY)
