import aiomysql

from config.settings import settings


async def create_database():
    async with aiomysql.connect(
        host=settings.API_DB_HOST,
        port=3306,
        user=settings.API_DB_USER,
        password=settings.API_DB_PASSWORD,
        db="mysql",
    ) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("CREATE DATABASE IF NOT EXISTS imob")
