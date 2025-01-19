from application import schemas, models
from application import crud
from fastapi import FastAPI, Depends, Query
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from application.database import get_db, engine, Base
from application.prod_kafka import send_to_kafka
from application.log import info_logger, error_logger
from pydantic import ValidationError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from aiokafka.errors import KafkaError


@asynccontextmanager
async def lifespan(app: FastAPI):
    info_logger.info("Создание таблиц базы данных ...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    info_logger.info("Выключение...")


app = FastAPI(lifespan=lifespan)


@app.post("/applications/", response_model=schemas.Application)
async def create_application(
        application: schemas.ApplicationCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.Application:
    """
    Создание новой заявки
    """
    try:
        db_application = await crud.create_application(db, application)
        info_logger.info(f"Created new application: {db_application.id}")
        await send_to_kafka(db_application)
        info_logger.info(f"Application id {db_application.id} send in Kafka.")
        return db_application

    except ValidationError as error:
        error_logger.error(f"Validation error: {error}")
        raise HTTPException(status_code=422, detail=str(error))
    except IntegrityError as error:
        error_logger.error(f"Database integrity error: {error}")
        raise HTTPException(status_code=400, detail="Data conflict (e.g., duplicate entry)")
    except (OperationalError, DataError) as error:
        error_logger.error(f"Database operation error: {error}")
        raise HTTPException(status_code=503, detail="Database error")
    except KafkaError as error:
        error_logger.error(f"Kafka error: {error}")
        raise HTTPException(status_code=503, detail="Message queue error")
    except Exception as error:
        error_logger.error(f"Unexpected error: {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/applications/", response_model=list[schemas.Application])
async def get_applications(
    user_name: str = Query(None),
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db)
) -> Sequence[models.Application]:
    """
    Возвращает список заявок с возможностью фильтрации по имени пользователя и пагинацией

    param user_name: Имя пользователя для фильтрации. По умолчанию None.
    param page: Номер страницы. По умолчанию 1.
    param size: Количество заявок на странице. По умолчанию 10.
    """
    try:
        if page < 1 or size < 1:
            error_logger.error(f"Invalid pagination parameters: page={page}, size={size}")
            raise HTTPException(status_code=400, detail="Invalid pagination parameters")

        info_logger.info(f"Request applications: user_name: {user_name}, page: {page}, size: {size}")
        applications = await crud.get_applications(db, user_name=user_name, page=page, size=size)
        return applications

    except (OperationalError, DataError) as error:
        error_logger.error(f"Database operation error: {error}")
        raise HTTPException(status_code=503, detail=f"Database error")

    except HTTPException as error:
        error_logger.error(f"Unexpected error: {error}")
        raise HTTPException(status_code=error.status_code, detail=error.detail)


