from ast import Pass
import email
from os import access
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from enum import IntEnum


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    pass

class PostBase(BaseModel):
    title: str
    content: str
    publish: bool = True

    
class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

    pass

class TokenData(BaseModel):
    id: Optional[str] = None
    pass

class Upvotes(IntEnum):
    remove = 0
    add = 1
class Vote(BaseModel):
    post_id: int
    dir: Upvotes
    # dir: conint(le=1, ge=0)
    pass
