
from fastapi.exceptions import HTTPException
from starlette import status
from ..hashing import Hash
from .. import models, schemas
from sqlalchemy.orm.session import Session


def create(request: schemas.CreateUser, db: Session):
    hashed_password = Hash.bcrypt(request.password)
    print(request.password, hashed_password)
    try:
        new_user = models.User(
            name=request.name, email=request.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Something went wrong. Use unique username please.')
    return new_user


def user_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with id {id} found.')
    return user
