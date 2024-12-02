from sqlalchemy import desc, insert, select

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model).order_by(desc(cls.model.id))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_by_id(cls, instance_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=instance_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all_filters(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .order_by(desc(cls.model.id))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            new_instance = await session.execute(query)
            await session.commit()
            return new_instance.scalar()
