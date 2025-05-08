import asyncpg
import os

DATABASE_URL = os.environ["DATABASE_URL"]

async def connect_db():
    return await asyncpg.connect(DATABASE_URL)
