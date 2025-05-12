from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from abc import ABC, abstractmethod


# lets now create our domain models using pydantic for our plants and the care logs as you suggested before


class WateringFrequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    AS_NEEDED = "as_needed"


class LightRequirement(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    DIRECT = "direct"


class CareLog(BaseModel):
    id: int
    action: str
    notes: str
    created_at: datetime


class Plant(BaseModel):
    id: int
    name: str
    species: str
    description: str
    watering_frequency: WateringFrequency
    light_requirement: LightRequirement
    last_watered: datetime
    next_watering: datetime
    created_at: datetime
    updated_at: datetime
    care_logs: list[CareLog]


class PlantRepository(ABC):
    @abstractmethod
    async def get(self, id: int) -> Plant:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, plant: Plant) -> Plant:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self) -> list[Plant]:
        raise NotImplementedError()
