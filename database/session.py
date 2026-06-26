from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from config import db_settings
from models import Base
engine = create_async_engine(db_settings.URL)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with sessionmaker() as session:
        yield session
    

