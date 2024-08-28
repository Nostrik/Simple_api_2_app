import sys
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from datetime import datetime
from loguru import logger
from .database import AsyncSessionLocal, engine, Base
from .models import User
from .sсhemas import UserCreate

app = FastAPI()
logger.remove()
# logger.add(sys.stdout,format="{level}:    {message}" , colorize=True)
logger.add(sys.stderr, level="INFO", format="<green>{level}</green>:     {message}", colorize=True)
tables_created = False


# Создание таблиц в базе данных (если они еще не созданы)
@app.on_event("startup")
async def startup():
    global tables_created
    logger.debug(f"Create tables called in process ID: {os.getpid()}")
    if not tables_created:
        logger.info("Create tables")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        tables_created = True


# Функция для получения асинхронной сессии базы данных
async def get_db() -> AsyncSession:
    logger.info("Get AsyncSession")
    async with AsyncSessionLocal() as session:
        yield session


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()  # Закрываем соединения с базой данных


@app.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(username=user.username, created_at=user.created_at)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
