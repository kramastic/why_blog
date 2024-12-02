from datetime import date
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from app.articles.routers import add_article, del_article, upd_article
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.routers import login_user, register_user
from app.users.schemas import SUserAuth

router = APIRouter(tags=["Frontend_redirect"])

templates = Jinja2Templates(directory="app/templates")


# ПЕРЕНАПРАВЛЕНИЕ войти
@router.post("/login_redirect")
async def login_redirect(
    response: Response, user_data: Annotated[SUserAuth, Form()]
):
    access_token = await login_user(response=response, user_data=user_data)
    response = RedirectResponse("/me", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("access_token", access_token, httponly=True)
    return response


# ПЕРЕНАПРАВЛЕНИЕ зарегистрироваться
@router.post("/register_redirect")
async def register_redirect(
    request: Request,
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    repeated_password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    second_name: Annotated[str, Form()],
    birthday_date: Annotated[date, Form()],
    nickname: Annotated[str | None, Form()],
    location: Annotated[str | None, Form()],
    introduction: Annotated[str | None, Form()],
    file: Annotated[UploadFile | str | None, File()],
):
    await register_user(
        email,
        password,
        repeated_password,
        name,
        second_name,
        birthday_date,
        nickname,
        location,
        introduction,
        file,
    )

    response = templates.TemplateResponse(
        name="after_register.html", context={"request": request}
    )
    return response


# ПЕРЕНАПРАВЛЕНИЕ выйти
@router.post("/logout_redirect")
async def logout_redirect(
    response: Response,
):
    response = RedirectResponse(
        "/sign_in", status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie("access_token")
    return response


# ПЕРЕНАПРАВЛЕНИЕ новая статья
@router.post("/new_article_redirect")
async def new_post_redirect(
    response: Response,
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    source_link: Annotated[str, None, Form()] = None,
    file: UploadFile | str | None = None,
    current_user: Users = Depends(get_current_user),
):
    await add_article(
        title=title,
        content=content,
        source_link=source_link,
        file=file,
        user=current_user,
    )
    response = RedirectResponse("/me", status_code=status.HTTP_303_SEE_OTHER)
    return response


# ПЕРЕНАПРАВЛЕНИЕ удалить статью
@router.post("/delete_article{article_id}")
async def delete_article(
    response: Response,
    article_id: int,
    user: Users = Depends(get_current_user),
):
    await del_article(article_id=article_id, user=user)
    response = RedirectResponse("/me", status_code=status.HTTP_302_FOUND)
    return response


# ПЕРЕНАПРАВЛЕНИЕ изменить статью
@router.post("/update_article_redirect{article_id}")
async def update_redirect(
    response: Response,
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    article_id: int,
    file: UploadFile | str | None = None,
    source_link: Annotated[str, None, Form()] = None,
    user: Users = Depends(get_current_user),
):
    await upd_article(
        article_id=article_id,
        user=user,
        title=title,
        content=content,
        source_link=source_link,
        file=file,
    )
    response = RedirectResponse("/me", status_code=status.HTTP_302_FOUND)
    return response
