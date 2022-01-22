from ..oauth2 import get_current_user
from typing import List
from fastapi import APIRouter, status, Depends
from .. import database, schemas
from ..repository import blog
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    print(current_user)
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create(request: schemas.Blog, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    return blog.create(request, current_user, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_by_id(id: int,   db: Session = Depends(database.get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return blog.get_by_id(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    return blog.update(id, current_user, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(database.get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return blog.delete(id, current_user, db)
