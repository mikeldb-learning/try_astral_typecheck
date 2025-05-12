# Here we will define the routes for the plants API, async and will be imported into the main main.py file here we only care about routes, no db

from typing import Annotated
from fastapi import APIRouter, Depends

from app.plants.domain import Plant
from app.plants.application import get_plants
from app.plants.infrastructure import PostgresPlantsUoW

router = APIRouter(prefix="/plants", tags=["plants"])


@router.get("/", response_model=list[Plant])
async def read_plants(uow: Annotated[PostgresPlantsUoW, Depends(PostgresPlantsUoW)]):
    return await get_plants(uow)


# @router.post("/", response_model=Plant)
# async def create_plant(plant: PlantCreate, db: AsyncSession = Depends(get_db)):
#     return await plant_crud.create_plant(db=db, plant=plant)


# @router.get("/{plant_id}", response_model=Plant)
# async def read_plant(plant_id: int, db: AsyncSession = Depends(get_db)):
#     db_plant = await plant_crud.get_plant(db, plant_id=plant_id)
#     if db_plant is None:
#         raise HTTPException(status_code=404, detail="Plant not found")
#     return db_plant


# @router.put("/{plant_id}", response_model=Plant)
# async def update_plant(
#     plant_id: int,
#     plant: PlantUpdate,
#     db: AsyncSession = Depends(get_db)
# ):
#     db_plant = await plant_crud.update_plant(db, plant_id=plant_id, plant=plant)
#     if db_plant is None:
#         raise HTTPException(status_code=404, detail="Plant not found")
#     return db_plant


# @router.delete("/{plant_id}")
# async def delete_plant(plant_id: int, db: AsyncSession = Depends(get_db)):
#     success = await plant_crud.delete_plant(db, plant_id=plant_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Plant not found")
#     return {"message": "Plant deleted successfully"}


# @router.post("/{plant_id}/care-logs/", response_model=CareLog)
# async def create_care_log(
#     plant_id: int,
#     care_log: CareLogCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#     db_care_log = await plant_crud.add_care_log(db, plant_id=plant_id, care_log=care_log)
#     if db_care_log is None:
#         raise HTTPException(status_code=404, detail="Plant not found")
#     return db_care_log


# @router.get("/{plant_id}/care-logs/", response_model=List[CareLog])
# async def read_care_logs(
#     plant_id: int,
#     skip: int = 0,
#     limit: int = 100,
#     db: AsyncSession = Depends(get_db)
# ):
#     # Verify plant exists
#     plant = await plant_crud.get_plant(db, plant_id=plant_id)
#     if plant is None:
#         raise HTTPException(status_code=404, detail="Plant not found")

#     care_logs = await plant_crud.get_care_logs(db, plant_id=plant_id, skip=skip, limit=limit)
#     return care_logs
