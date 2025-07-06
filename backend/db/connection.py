import asyncpg
import os
from peewee import PostgresqlDatabase
from urllib.parse import urlparse

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:pass@host:port/dbname")
url = urlparse(DATABASE_URL)

async def connect_db():
    return await asyncpg.connect(DATABASE_URL)
db = PostgresqlDatabase(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)