from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .schemas import UserCreate
from .database import AsyncSessionLocal, engine, Base
from .models import User

app = FastAPI()

# Создание таблиц в базе данных (если они еще не созданы)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция для получения асинхронной сессии базы данных
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()  # Закрываем соединения с базой данных


@app.post("/users/", response_model=schemas.UserCreate)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(username=user.username, created_at=user.created_at)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
