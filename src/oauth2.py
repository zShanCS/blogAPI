from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(test_token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials... try to login again.',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    return token.verify_token(test_token, credential_exception)
