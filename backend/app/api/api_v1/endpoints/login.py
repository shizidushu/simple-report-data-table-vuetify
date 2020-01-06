from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.core import config
from app.api.utils.security import get_current_user
from app.mongodb_models.user import User as DBUser
from app.fields.user import User
from app.fields.token import Token
from app.core.jwt import create_access_token

router = APIRouter()


@router.post("/access-token/", response_model=Token)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) ->Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"username": user.Username}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test-token/", response_model=User)
def test_token(current_user: User = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user