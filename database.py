from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings

SQLALCHEMY_DATABASE_URL = settings.get_db_url()


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True
)

Base = declarative_base()


async def get_db() -> AsyncSessionLocal:
    """
    Генератор сессий базы данных.
    :return: AsyncSession: Асинхронная сессия базы данных.
    """
    async with AsyncSessionLocal() as db:
        yield db