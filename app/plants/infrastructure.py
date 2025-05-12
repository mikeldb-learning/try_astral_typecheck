from typing import Annotated
from datetime import datetime

from fastapi import Depends
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.plants.domain import (
    LightRequirement,
    Plant,
    CareLog,
    PlantRepository,
    WateringFrequency,
)
from app.plants.application import PlantsUoW


# lets now create our database models with everything we're going to need and a function to transform them into our domain models called to_do``
class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    watering_frequency: Mapped[WateringFrequency] = mapped_column(
        Enum(WateringFrequency), nullable=False
    )
    light_requirement: Mapped[LightRequirement] = mapped_column(
        Enum(LightRequirement), nullable=False
    )
    last_watered: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    next_watering: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    care_logs: Mapped[list["CareLog"]] = relationship(
        "CareLog", back_populates="plant", cascade="all, delete-orphan"
    )

    def to_domain(self) -> Plant:
        return Plant(
            id=self.id,
            name=self.name,
            species=self.species,
            description=self.description,
            watering_frequency=self.watering_frequency,
            light_requirement=self.light_requirement,
            last_watered=self.last_watered,
            next_watering=self.next_watering,
            created_at=self.created_at,
            updated_at=self.updated_at,
            care_logs=[],
        )


class CareLog(Base):
    __tablename__ = "care_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("plants.id"), nullable=False
    )
    action: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # watering, fertilizing, pruning, etc.
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    plant: Mapped["Plant"] = relationship("Plant", back_populates="care_logs")

    def to_domain(self) -> CareLog:
        return CareLog(
            id=self.id, action=self.action, notes=self.notes, created_at=self.created_at
        )


class PostgresPlantRepository(PlantRepository):
    async def get_all(self) -> list[Plant]:
        return [Plant(id=1, name="Plant 1", description="Plant 1 description")]

    async def get(self, id: int) -> Plant:
        return Plant(id=1, name="Plant 1", description="Plant 1 description")

    async def save(self, plant: Plant) -> Plant:
        return plant

    async def delete(self, id: int) -> None:
        pass


class PostgresPlantsUoW(PlantsUoW):
    plant_repository: PostgresPlantRepository

    def __init__(
        self,
        plant_repository: Annotated[PlantRepository, Depends(PostgresPlantRepository)],
    ):
        self.plant_repository = plant_repository
