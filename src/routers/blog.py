from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from .. import database, models, schemas

from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['blogs'])
def get(db: Session = Depends(database.get_db)):
    return db.query(models.Blog).all()


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title,
                           body=request.body, author_user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def get_by_id(id: int,   db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The blog with id {id} does not exists or is private")
    return blog


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the blog of id {id} not found')
    print(request)
    blog.update(request.dict())
    db.commit()
    return {'details': 'done'}


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_by_id(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the blog of id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'details': 'done'}
