from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.responses import Response
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED

from app import crud
from app.fields.user import UserBase, User, UserCreate, UserInDB, UserUpdate


router = APIRouter()


@router.get("/read_users/", response_model=List[User])
def read_users(
    skip: int = None,
    limit: int = None,
):
    """
    Retrieve users.
    """
    users = crud.user.get_multi(skip=skip, limit=limit)
    return users


@router.put("/create_user/", response_model=UserInDB)
def create_user(
    user_in: UserCreate,
):
    """
    Create new user.
    """
    user = crud.user.get_db_user(username = user_in.Username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(user_in=user_in)
    # if config.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return user

@router.put("/upsert_users/", response_model=List[UserInDB])
async def upsert_users(*, users_in: List[UserCreate]):
    """
    Create new users if not exists before.
    """
    users = []
    for user_in in users_in:
        user = crud.user.get_db_user(username = user_in.Username)
        if user:
            user = crud.user.update(user, user_in)
        else:
            user = crud.user.create(user_in=user_in)
        users.append(user)

    return users


@router.get("/me/", response_model=User)
def read_user_me(request: Request):
    """
    Get current user.
    """
    return request.state.user


