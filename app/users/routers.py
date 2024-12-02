import shutil
from datetime import date, datetime

from fastapi import APIRouter, Response, UploadFile
from pydantic import EmailStr

from app.exceptions import (
    IncorrectEmailOrPasswordException,
    PasswordsDoesNotMatch,
    UserAlreadyExistsException,
)
from app.tasks.tasks import send_confirmation_email
from app.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth, SUserResponse

router = APIRouter(
    # prefix='/auth',
    tags=["Auth&Users"]
)


@router.post("/register")
async def register_user(
    email: EmailStr,
    password: str,
    repeated_password: str,
    name: str,
    second_name: str,
    birthday_date: date,
    nickname: str | None = None,
    location: str | None = None,
    introduction: str | None = None,
    file: UploadFile | str | None = None,
):
    existing_user = await UsersDAO.find_one_or_none(email=email)
    if existing_user:
        raise UserAlreadyExistsException
    if password != repeated_password:
        raise PasswordsDoesNotMatch
    if file:
        image_title = f'{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}'
        im_path = f"app/static/images/avatars/{image_title}.webp"
        with open(f"{im_path}", "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    else:
        image_title = None

    hashed_password = get_password_hash(password)
    new_user = await UsersDAO.add(
        email=email,
        hashed_password=hashed_password,
        name=name,
        second_name=second_name,
        birthday_date=birthday_date,
        avatar_id=image_title,
        nickname=nickname,
        location=location,
        introduction=introduction,
    )
    new_user_dict = SUserResponse.model_validate(new_user).model_dump()
    send_confirmation_email.delay(new_user_dict["email"])

    return new_user_dict


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return "logout is accomplished"
