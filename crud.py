import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def create_application(db: AsyncSession, application: schemas.ApplicationCreate):
    db_application = models.Application(**application.dict())
    db.add(db_application)
    await db.commit()
    await db.refresh(db_application)
    return db_application

async def get_applications(db: AsyncSession, user_name: str = None, page: int = 1, size: int = 10):
    query = select(models.Application)
    if user_name:
        query = query.where(models.Application.user_name == user_name)
    query = query.offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    return result.scalars().all()