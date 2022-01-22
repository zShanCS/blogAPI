from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from .. import models, schemas


def get_all(db: Session):
    return db.query(models.Blog).all()


def create(blog: schemas.Blog, current_user_email, db: Session):
    user = db.query(models.User).filter(
        models.User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User Not Found")
    new_blog = models.Blog(title=blog.title,
                           body=blog.body, author_user_id=user.id)
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


def update(id: int, current_user_email: str, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the blog of id {id} not found')
    # blog exists. now check if user is allowed to edit this blog
    user = db.query(models.User).filter(
        models.User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User Not Found")
    if not blog.first().author_user_id == user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to modify this blog")
    blog.update(request.dict())
    db.commit()
    return {'details': 'done'}


def delete(id: int, current_user_email: str, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the blog of id {id} not found')
    # blog exists. now check if user is allowed to edit this blog
    user = db.query(models.User).filter(
        models.User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User Not Found")
    if not blog.first().author_user_id == user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to delete this blog")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'details': 'done'}
