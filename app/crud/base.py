from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, false, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.models.user import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=Optional[BaseModel])


class CRUDBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
            self, object_id: int, session: AsyncSession
    ):
        return (
            await session.execute(
                select(self.model).where(self.model.id == object_id)
            )
        ).scalars().first()

    async def get_multiple(self, session: AsyncSession) -> List[ModelType]:
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def create(
            self,
            object_in,
            session: AsyncSession,
            user: User = None,
            need_commit: bool = True
    ):
        db_object = self.model(**object_in.dict())
        db_object.user_id = user.id if user else None
        db_object.invested_amount = 0
        session.add(db_object)
        if need_commit:
            await session.commit()
            await session.refresh(db_object)

        return db_object

    async def update(self, db_object, object_in, session: AsyncSession):
        obj_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def remove(self, db_object, session: AsyncSession):
        await session.delete(db_object)
        await session.commit()
        return db_object

    async def get_not_fully_invested_objects(
        self,
        session: AsyncSession
    ):
        not_fully_invested_objects = await session.execute(
            select(
                self.model
            ).where(
                self.model.fully_invested == false()).order_by(
                self.model.create_date
            )
        )
        return not_fully_invested_objects.scalars().all()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ):
        projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested
            ).order_by(
                (
                    extract('day', self.model.close_date)
                ) - (
                    extract('day', self.model.create_date)
                )
            )
        )
        return projects.scalars().all()
