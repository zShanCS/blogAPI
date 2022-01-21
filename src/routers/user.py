
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session
from .. import schemas
from ..database import get_db
from ..repository import user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase)
def create_user(request: schemas.CreateUser, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def user_by_id(id: int, db: Session = Depends(get_db)):
    return user.user_by_id(id, db)
