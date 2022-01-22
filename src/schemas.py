from typing import List, Optional
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class ShowBlog(Blog):
    creator: UserBase


class CreateUser(UserBase):
    password: str


class ShowUser(UserBase):
    blogs: List[Blog] = []


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
