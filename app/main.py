from fastapi import FastAPI
from app.core.database import engine, Base
from app.plants.routes import router as plants_router

app = FastAPI(title="Plant Care API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


# Include the plants router
app.include_router(plants_router)
