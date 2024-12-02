import os
import shutil
from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy import and_, select

from app.articles.dao import ArticlesDAO
from app.articles.models import Articles
from app.articles.schemas import SShowArticle
from app.database import async_session_maker
from app.exceptions import ArticleIsNotPostedException
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/articles", tags=["Статьи"])


@router.get("/all_user_articles")
async def get_articles(user: Users = Depends(get_current_user)):
    user_articles: list[SShowArticle] = await ArticlesDAO.find_all_filters(
        user_id=user.id
    )
    return user_articles


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_article(
    title: str,
    content: str,
    source_link: str,
    file: UploadFile | str | None = None,
    user: Users = Depends(get_current_user),
):
    if file.filename:
        image_title = f'{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}'
        im_path = f"app/static/images/articles/{image_title}.webp"
        with open(f"{im_path}", "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    else:
        image_title = None

    article = await ArticlesDAO.add(
        title=title.strip(),
        content=content.strip(),
        source_link=source_link.strip(),
        image_id=image_title,
        user_id=user.id,
    )

    if not article:
        raise ArticleIsNotPostedException

    article_dict = SShowArticle.model_validate(article).model_dump()
    return article_dict


@router.post("/delete")
async def del_article(
    article_id: int,
    user: Users = Depends(get_current_user),
):
    delete_article = await ArticlesDAO.delete(
        article_id=article_id, user_id=user.id
    )
    if delete_article:
        return True
    else:
        return False


@router.post("/update")
async def upd_article(
    article_id: int,
    title: str,
    content: str,
    source_link: str | None,
    file: UploadFile | str | None = None,
    user: Users = Depends(get_current_user),
):
    data = {
        "title": title,
        "content": content,
        "source_link": source_link,
    }
    if file.filename:
        image_title = f'{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}'
        im_path = f"app/static/images/articles/{image_title}.webp"
        with open(f"{im_path}", "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    else:
        image_title = None

    if image_title:
        data["image_id"] = image_title
        async with async_session_maker() as session:
            image_id_query = select(Articles).where(
                and_(Articles.id == article_id, Articles.user_id == user.id)
            )
            res = await session.execute(image_id_query)
            image_id = res.scalar_one_or_none().image_id
            if image_id:
                os.remove(f"app/static/images/articles/{image_id}.webp")
    data = {
        "title": title,
        "content": content,
        "source_link": source_link,
    }
    update_article = await ArticlesDAO.update(
        user_id=user.id, article_id=article_id, data=data
    )
    if update_article:
        return True
    else:
        return False
