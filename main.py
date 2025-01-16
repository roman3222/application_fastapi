import schemas, crud
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database import get_db, engine, Base
from prod_kafka import send_to_kafka
from log import info_logger, error_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    info_logger.info("Создание таблиц базы данных ...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    info_logger.info("Выключение...")


app = FastAPI(lifespan=lifespan)


@app.post("/applications/", response_model=schemas.Application)
async def create_application(application: schemas.ApplicationCreate, db: AsyncSession = Depends(get_db)):
    db_application = await crud.create_application(db, application)
    await send_to_kafka(db_application)
    return db_application


@app.get("/applications/", response_model=list[schemas.Application])
async def get_applications(
    user_name: str = Query(None),
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db)
):
    applications = await crud.get_applications(db, user_name=user_name, page=page, size=size)
    return applications