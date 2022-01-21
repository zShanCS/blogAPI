from typing import List
from fastapi import FastAPI, Depends, status, HTTPException
import schemas
import models
from hashing import Hash
from database import engine, SessionLocal
from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_by_id(id: int,   db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The blog with id {id} does not exists or is private")
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the blog of id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'details': 'done'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the blog of id {id} not found')
    print(request)
    blog.update(request.dict())
    db.commit()
    return 'done'


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase)
def create_user(request: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    print(request.password, hashed_password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserBase)
def user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with id {id} found.')
    return user
