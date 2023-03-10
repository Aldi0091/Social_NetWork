from typing import Optional

from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse

from auth.login import get_current_user, get_password_hash
from db.database import DB

profile_router = APIRouter()


@profile_router.get('/profile')
async def get_my_profile(access_token: Optional[str] = Header(None, description='JWT auth token')):
    '''
    Get posts and user data
    '''
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You're not logged in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_current_user(access_token)
    posts = await DB.get_post(user[0])
    if posts is None:
        posts = list()
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'id': user[0],
        'username': user[3],
        'login': user[1],
        'posts': posts
    })


@profile_router.put('/profile')
async def change_profile(
        access_token: Optional[str] = Header(None, description='JWT auth token'),
        username: Optional[str] = Header(None, description='New username'),
        password: Optional[str] = Header(None, description='New password')):
    '''
    Change user data if registered
    '''
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You're not logged in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = list(await get_current_user(access_token))
    if password is not None:
        user[2] = get_password_hash(password)
    else:
        user[2] = None
    if username is not None:
        user[3] = username
    if not await DB.update_user_db(user[2], user[3], user[0]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is not unique"
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'name': user[3]
    })
