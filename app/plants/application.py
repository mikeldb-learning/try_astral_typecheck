from abc import ABC
from pydantic import BaseModel
from app.plants.domain import (
    LightRequirement,
    PlantRepository,
    Plant,
    WateringFrequency,
)


class PlantsUoW(ABC):
    plant_repository: PlantRepository


async def get_plants(uow: PlantsUoW):
    return await uow.plant_repository.get_all()


class GetPlantRequest(BaseModel):
    id: int


async def get_plant(uow: PlantsUoW, request: GetPlantRequest):
    return await uow.plant_repository.get(request.id)


class CreatePlantRequest(BaseModel):
    name: str
    species: str
    description: str
    watering_frequency: WateringFrequency
    light_requirement: LightRequirement


async def create_plant(uow: PlantsUoW, request: CreatePlantRequest):
    plant = Plant(
        name=request.name,
        species=request.species,
        description=request.description,
        watering_frequency=request.watering_frequency,
        light_requirement=request.light_requirement,
    )
    return await uow.plant_repository.save(plant)
