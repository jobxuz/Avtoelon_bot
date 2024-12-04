import asyncio
from app.utils.db_manager import db


async def initialize():
    await db.connect()
    await db.create_tables()
    await db.disconnect()

asyncio.run(initialize())