from typing import Annotated
from datetime import datetime

from fastapi import Depends
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Enum, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, async_session
from app.plants.domain import (
    LightRequirement,
    Plant,
    CareLog,
    PlantRepository,
    WateringFrequency,
)
from app.plants.application import PlantsUoW


# lets now create our database models with everything we're going to need and a function to transform them into our domain models called to_do``
class DBPlant(Base):
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

    care_logs: Mapped[list["DBCareLog"]] = relationship(
        "DBCareLog", back_populates="plant", cascade="all, delete-orphan"
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


class DBCareLog(Base):
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

    plant: Mapped["DBPlant"] = relationship("DBPlant", back_populates="care_logs")

    def to_domain(self) -> CareLog:
        return CareLog(
            id=self.id, action=self.action, notes=self.notes, created_at=self.created_at
        )


class PostgresPlantRepository(PlantRepository):
    async def get_all(self) -> list[Plant]:
        async with async_session() as session:
            stmt = select(DBPlant)
            result = await session.execute(stmt)
            db_plants = result.scalars().all()
            return [plant.to_domain() for plant in db_plants]

    async def get(self, id: int) -> Plant:
        async with async_session() as session:
            stmt = select(DBPlant).where(DBPlant.id == id)
            result = await session.execute(stmt)
            db_plant = result.scalar_one_or_none()
            if not db_plant:
                raise ValueError(f"Plant with id {id} not found")
            return db_plant.to_domain()

    async def save(self, plant: Plant) -> Plant:
        async with async_session() as session:
            if plant.id:
                # Update existing plant
                stmt = select(DBPlant).where(DBPlant.id == plant.id)
                result = await session.execute(stmt)
                db_plant = result.scalar_one_or_none()

                if db_plant:
                    db_plant.name = plant.name
                    db_plant.species = plant.species
                    db_plant.description = plant.description
                    db_plant.watering_frequency = plant.watering_frequency
                    db_plant.light_requirement = plant.light_requirement
                    db_plant.last_watered = plant.last_watered
                    db_plant.next_watering = plant.next_watering
                    db_plant.updated_at = datetime.utcnow()
            else:
                # Create new plant
                db_plant = DBPlant(
                    name=plant.name,
                    species=plant.species,
                    description=plant.description,
                    watering_frequency=plant.watering_frequency,
                    light_requirement=plant.light_requirement,
                    last_watered=plant.last_watered,
                    next_watering=plant.next_watering,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(db_plant)

            await session.commit()
            return db_plant.to_domain()

    async def delete(self, id: int) -> None:
        async with async_session() as session:
            stmt = select(DBPlant).where(DBPlant.id == id)
            result = await session.execute(stmt)
            db_plant = result.scalar_one_or_none()
            if db_plant:
                await session.delete(db_plant)
                await session.commit()


class PostgresPlantsUoW(PlantsUoW):
    plant_repository: PostgresPlantRepository

    def __init__(
        self,
        plant_repository: Annotated[PlantRepository, Depends(PostgresPlantRepository)],
    ):
        self.plant_repository = plant_repository
