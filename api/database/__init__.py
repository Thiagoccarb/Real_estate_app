from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine

from config.settings import settings


def compile_db_uri() -> str:
    return f"mysql+aiomysql://{settings.API_DB_USER}:{settings.API_DB_PASSWORD}@{settings.API_DB_HOST}:3306/{settings.API_DB_DATABASE}"


engine = create_async_engine(
    compile_db_uri(),
    future=True,
    echo=False,
    echo_pool=False,
    logging_name="DATABASE",
    pool_size=10,
    pool_recycle=3600,
)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as session:
        yield session


db = SessionLocal()
