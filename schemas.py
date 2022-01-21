from models import User
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(Blog):
    class Config():
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class CreateUser(UserBase):
    password: str
