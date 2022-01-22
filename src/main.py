from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user, authentication

# create all db tables if not already there
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
