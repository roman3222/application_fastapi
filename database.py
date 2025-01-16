from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

# Асинхронный URL для подключения к PostgreSQL
SQLALCHEMY_DATABASE_URL = settings.get_db_url()

# Создаем асинхронный движок
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создаем асинхронную сессию
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True  # Включаем поддержку SQLAlchemy 2.0
)

Base = declarative_base()

# Асинхронная зависимость для получения сессии
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db