import asyncio
from database import init_db, close_db

async def create_tables():
    pool = await init_db()
    async with pool.acquire() as conn:
        try:
            with open("models.sql", "r") as f:
                sql = f.read()
            await conn.execute(sql)
            print("Tables created (or recreated) successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
    await close_db()

if __name__ == "__main__":
    asyncio.run(create_tables())
