from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://admin:admin@python_advanced_diploma-db-1:5432/simple_api_2_db"  # Замените username, password и dbname на свои значения
# DATABASE_URL_2 = "postgresql+asyncpg://admin:admin@db:5432"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
