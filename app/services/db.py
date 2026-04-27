from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Postgres
POSTGRES_DATABASE_URL = "postgresql+asyncpg://fastapi:postgres@localhost:5432/fastapi"
postgres_engine = create_async_engine(POSTGRES_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(postgres_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# Mongo
MONGO_DATABASE_URL = "mongodb://localhost:27017/"
DB_NAME = "blog"

client = AsyncIOMotorClient(MONGO_DATABASE_URL)
database = client[DB_NAME]

def get_mongo_db() -> AsyncIOMotorDatabase:
    return database