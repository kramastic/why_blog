from fastapi import HTTPException, status


class BaseException(HTTPException):

    def __str__(self):
        return self.status_code

    status_code = (None,)
    detail = None


class UserAlreadyExistsException(BaseException):

    def __init__(self):
        self.status_code = status.HTTP_409_CONFLICT

    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с указанным e-mail уже существует"


class IncorrectEmailOrPasswordException(BaseException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверные имя пользователя или пароль"


class AuthenticationTokenAbsenceException(BaseException):

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED

    staus_code = status.HTTP_401_UNAUTHORIZED
    detail = "Отсутствует токен аутентификации"


class IncorrectTokenFormatException(BaseException):

    def __init__(self):
        self.status_code = 401

    staus_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена аутентификации"


class TokenExpiredException(BaseException):

    def __init__(self):
        self.status_code = 401

    staus_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен аутентификации устарел"


class UserIsNotFoundException(BaseException):

    def __init__(self):
        self.status_code = 401

    staus_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не найден"


class ArticleIsNotPostedException(BaseException):

    def __init__(self):
        self.status_code = 409

    status_code = status.HTTP_409_CONFLICT
    detail = "Статья не опубликована"


class PasswordsDoesNotMatch(BaseException):

    def __init__(self):
        self.status_code = 409

    status_code = status.HTTP_409_CONFLICT
    detail = "Пароли не совпадают"
