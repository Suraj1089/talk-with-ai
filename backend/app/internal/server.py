import logging
from contextlib import asynccontextmanager
from logging.config import dictConfig
from fastapi import FastAPI
from app.internal.config import LogConfig

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import create_db_and_tables

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("mycoolapp")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


origins: list[str] = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://localhost:4173",
    "http://localhost:4174"
]

app = FastAPI(
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
