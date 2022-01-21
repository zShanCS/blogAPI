from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from .. import models, schemas


def get_all(db: Session):
    return db.query(models.Blog).all()


def create(blog: schemas.Blog, db: Session):
    new_blog = models.Blog(title=blog.title,
                           body=blog.body, author_user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_by_id(id: int, db: Session):
    myblog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not myblog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The blog with id {id} does not exists or is private")
    return myblog


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the blog of id {id} not found')
    print(request)
    blog.update(request.dict())
    db.commit()
    return {'details': 'done'}


def delete(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the blog of id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'details': 'done'}
