from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users
from app.users.schemas import SUserResponse


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def find_by_id(cls, instance_id: int):
        async with async_session_maker() as session:
            query = select(
                Users.id,
                Users.avatar_id,
                Users.birthday_date,
                Users.email,
                Users.introduction,
                Users.location,
                Users.name,
                Users.nickname,
                Users.second_name,
            ).filter_by(id=instance_id)
            result = await session.execute(query)
            result_orm = result.all()
            result_validation = [
                SUserResponse.model_validate(row, from_attributes=True)
                for row in result_orm
            ]

            return result_validation[0]
