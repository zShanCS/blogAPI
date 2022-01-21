
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm.session import Session
from .. import schemas, models
from ..hashing import Hash
from ..database import get_db

router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase, tags=['users'])
def create_user(request: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    print(request.password, hashed_password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=['users'])
def user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with id {id} found.')
    return user
