from typing import List
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
