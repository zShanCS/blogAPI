
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, token
from ..models import User
from ..database import get_db
from ..hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Login']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Invalid Email')
    if not Hash.verify(hash=user.password, plain_pass=request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Invalid Password')
    # create hwt and return
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
