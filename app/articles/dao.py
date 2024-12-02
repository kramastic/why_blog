import os

from sqlalchemy import and_, delete, select, update

from app.articles.models import Articles
from app.dao.base import BaseDAO
from app.database import async_session_maker


class ArticlesDAO(BaseDAO):
    model = Articles

    @classmethod
    async def delete(cls, user_id, article_id):
        async with async_session_maker() as session:
            query = select(Articles).where(
                and_(Articles.id == article_id, Articles.user_id == user_id)
            )
            res = await session.execute(query)
            image_id = res.scalar_one_or_none().image_id
            query_delete = delete(Articles).where(
                and_(Articles.id == article_id, Articles.user_id == user_id)
            )
            await session.execute(query_delete)
            await session.commit()
        if image_id:
            os.remove(f"app/static/images/articles/{image_id}.webp")

        return True

    @classmethod
    async def update(cls, user_id, article_id, data):
        async with async_session_maker() as session:
            query_update = (
                update(Articles)
                .where(
                    and_(
                        Articles.id == article_id, Articles.user_id == user_id
                    )
                )
                .values(**data)
            )
            await session.execute(query_update)
            await session.commit()

            return True
