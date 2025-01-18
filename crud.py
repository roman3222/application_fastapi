import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Sequence

async def create_application(db: AsyncSession, application: schemas.ApplicationCreate) -> models.Application:
    """
    Создает новую заявку в базе данных.
    :param db: Сессия базы данных.
    :param application: Данные заявки.
    :return: Созданная заявка.
    """
    db_application = models.Application(**application.model_dump())
    db.add(db_application)
    await db.commit()
    await db.refresh(db_application)
    print(type(db_application))
    return db_application


async def get_applications(
        db: AsyncSession,
        user_name: str = None,
        page: int = 1,
        size: int = 10
) -> Sequence[models.Application]:
    """
    Возвращает список заявок с возможностью фильтрации по имени пользователя и пагинацией.
    :param db: (AsyncSession) Сессия базы данных.
    :param user_name: Имя пользователя для фильтрации. По умолчанию None.
    :param page: Номер страницы. По умолчанию 1.
    :param size: Количество заявок на странице. По умолчанию 10.
    :return: Sequence[models.Application]: Список заявок.
    """
    query = select(models.Application)
    if user_name:
        query = query.where(models.Application.user_name == user_name)
    query = query.offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    return result.scalars().all()