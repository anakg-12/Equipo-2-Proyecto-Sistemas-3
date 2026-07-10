import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.bd.database import Base
from app.config import settings
import app.models

async def create_tables():
    engine = create_async_engine(settings.async_database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

async def run_seed():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "seed.py",
        stdout=sys.stdout, stderr=sys.stderr
    )
    await proc.wait()

async def main():
    await create_tables()
    await run_seed()

if __name__ == "__main__":
    asyncio.run(main())