from fastapi import FastAPI
from src import models
from src.database import engine
from src.routers import blog, user, authentication

# create all db tables if not already there
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
