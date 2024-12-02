from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SShowArticle(BaseModel):
    id: int
    title: str
    content: str
    image_id: str | None
    create_datetime: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)
