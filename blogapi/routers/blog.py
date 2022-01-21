from typing import List
from fastapi import APIRouter, status, Depends
from .. import database, models, schemas

from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['blogs'])
def get(db: Session = Depends(database.get_db)):
    return db.query(models.Blog).all()
