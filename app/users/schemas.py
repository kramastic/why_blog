from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class SUserResponse(BaseModel):
    id: int
    email: str
    name: str
    second_name: str
    birthday_date: date
    nickname: str | None = None
    location: str | None = None
    introduction: str | None = None
    avatar_id: str | None = None

    model_config = ConfigDict(from_attributes=True)
