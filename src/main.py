from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas, models
from .hashing import Hash
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import blog, user


app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
