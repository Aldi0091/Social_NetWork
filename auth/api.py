from fastapi import APIRouter, status, HTTPException
from . import schemas
from .login import login_for_access_token, register_user

user_router = APIRouter()


@user_router.post('/registration', response_model=schemas.UserNew)
async def register_new(user: schemas.UserNew):
    '''
    Register new user
    '''
    if not await register_user(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or login is not unique",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@user_router.post('/login', response_model=schemas.Token)
async def authenticate(user: schemas.User):
    '''
    Get auth token
    '''
    return await login_for_access_token(user.login, user.password)