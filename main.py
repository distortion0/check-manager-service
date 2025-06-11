from contextlib import asynccontextmanager

from fastapi import FastAPI

from db_utils.db_init import init_db
from routers import auth, check

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(check.router, prefix="/checks", tags=["checks"])
