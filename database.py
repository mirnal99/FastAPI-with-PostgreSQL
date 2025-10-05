import asyncpg
from typing import Optional

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/BookLog"

pool: Optional[asyncpg.Pool] = None

async def init_db():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
    return pool

async def close_db():
    global pool
    if pool:
        await pool.close()
        pool = None
