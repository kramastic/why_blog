from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.articles.dao import ArticlesDAO
from app.articles.schemas import SShowArticle
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(tags=["Frontend"])


templates = Jinja2Templates(directory="app/templates")


# страница пользователя
@router.get("/id{user_id}")
async def get_user_page(
    user_id: int,
    request: Request,
    current_user: Users | None = Depends(get_current_user),
):
    user = await UsersDAO.find_by_id(instance_id=user_id)
    articles: list[SShowArticle] = await ArticlesDAO.find_all_filters(
        user_id=int(user.id)
    )
    return templates.TemplateResponse(
        name="user_page.html",
        context={
            "request": request,
            "user": user,
            "articles": articles,
            "current_user": current_user,
        },
    )


# страница моя
@router.get("/me")
async def get_my_page(
    request: Request, current_user: Users | None = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse("/sign_in")
    articles: list[SShowArticle] = await ArticlesDAO.find_all_filters(
        user_id=int(current_user.id)
    )
    title = "Моя страница"
    return templates.TemplateResponse(
        name="user_page.html",
        context={
            "request": request,
            "title": title,
            "user": current_user,
            "articles": articles,
            "current_user": current_user,
        },
    )


# страница всех пользователей
@router.get("/all_users")
async def get_all_users(
    request: Request, current_user: Users | None = Depends(get_current_user)
):
    users = await UsersDAO.find_all()
    return templates.TemplateResponse(
        name="all_users.html",
        context={
            "request": request,
            "users": users,
            "current_user": current_user,
        },
    )


# страница войти
@router.get("/sign_in")
async def sign_in(
    request: Request,
):
    response = templates.TemplateResponse(
        name="sign_in.html", context={"request": request}
    )
    return response


# страница зарегистрироваться
@router.get("/register")
async def register(
    request: Request,
):
    return templates.TemplateResponse(
        name="register.html", context={"request": request}
    )


# страница новая статья
@router.get("/new_article")
async def new_post(
    request: Request, current_user: Users = Depends(get_current_user)
):
    response = templates.TemplateResponse(
        name="new_article.html",
        context={"request": request, "current_user": current_user},
    )
    return response

#страница изменить статью
@router.get("/update_article{article_id}")
async def update_article(
    request: Request,
    article_id: int,
    current_user: Users = Depends(get_current_user),
):
    article = await ArticlesDAO.find_by_id(article_id)
    response = templates.TemplateResponse(
        name="update_article.html",
        context={
            "request": request,
            "current_user": current_user,
            "article": article,
        },
    )
    return response

#страница о проекте
@router.get("/about_project")
async def about_project(
    request: Request,
    current_user: Users = Depends(get_current_user)
):
    return templates.TemplateResponse(
        name="about_project.html", context={"request": request, 
                                            "current_user": current_user}
    )
