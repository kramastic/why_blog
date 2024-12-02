from sqladmin import ModelView

from app.articles.models import Articles
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [
        Users.id,
        Users.email,
        Users.name,
        Users.second_name,
        Users.articles,
    ]
    column_details_exclude_list = [Users.hashed_password]
    # can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class ArticlesAdmin(ModelView, model=Articles):
    column_list = [Articles.id, Articles.user, Articles.create_datetime]
    column_details_exclude_list = [Articles.content]
    name = "Artilcle"
    name_plural = "Articles"
