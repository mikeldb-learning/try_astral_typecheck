from abc import ABC
from app.plants.domain import PlantRepository


class PlantsUoW(ABC):
    plant_repository: PlantRepository


async def get_plants(uow: PlantsUoW):
    return await uow.plant_repository.get_all()


async def get_plant(uow: PlantsUoW, id: int):
    return await uow.plant_repository.get(id)
