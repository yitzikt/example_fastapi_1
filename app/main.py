from fastapi import FastAPI

from app.routers.votes import vote
from . import models
from .config import settings
from .database import engine
from .routers import auth, post, user, votes
from fastapi.middleware.cors import CORSMiddleware
# only need without alembic
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello yitz"}




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "Hello what!"}


# uvicorn app.main:app --reload
