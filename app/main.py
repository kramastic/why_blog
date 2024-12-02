from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin_panel.auth import authentication_backend
from app.admin_panel.views import ArticlesAdmin, UsersAdmin
from app.articles.routers import router as articles_routers
from app.config import settings
from app.database import engine
from app.pages.routers import router as pages_routers
from app.pages.routers_redirect import router as pages_routers_redirect
from app.users.routers import router as users_routers

app = FastAPI()

app.include_router(users_routers)
app.include_router(articles_routers)
app.include_router(pages_routers)
app.include_router(pages_routers_redirect)

app.mount("/static", StaticFiles(directory="app/static"), "static")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    )
    yield


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(ArticlesAdmin)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
