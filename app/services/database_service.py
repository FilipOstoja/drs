from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from app.database import Base, engine

# Kreiraj asinkroni engine i sesiju
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Funkcija za testiranje konekcije
async def test_db_connection():
    try:
        async with SessionLocal() as session:
            # Proveri konekciju
            result = await session.execute(select(1))
            return {"status": "success", "message": "Connection successful!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Funkcija za kreiranje tabela
async def create_tables():
    async with engine.begin() as conn:
        # Koristi asinkroni metod za izvršavanje
        await conn.run_sync(Base.metadata.create_all)