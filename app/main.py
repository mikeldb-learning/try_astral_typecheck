from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db, engine, Base

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/")
async def root():
    print("Hello World")
    return {"message": "Hello World"}


@app.get("/db-test")
async def db_test(db: AsyncSession = Depends(get_db)):
    # Test database connection
    result = await db.execute(text("SELECT 1"))
    return {"database_connection": "success", "result": result.scalar()}
