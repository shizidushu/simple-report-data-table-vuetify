from typing import List, Optional
import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, ExpiredSignatureError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from starlette.requests import Request

from app import crud
from app.core import config
from app.core.jwt import ALGORITHM
from app.fields.token import TokenPayload
from app.fields.user import User
from app.mongodb_models.user import User as DBUser
from app.core.casbin_auth import join_tags
from app.core.permission import enforcer

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


def get_current_user(request: Request, token: str = Security(reusable_oauth2)) -> Optional[User]:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail="Expired token"
    )
    except PyJWTError as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
        )
    user = crud.user.get_user(username=token_data.username)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    
    request.state.user = user

    return user


def get_current_active_user(current_user: User = Security(get_current_user)) -> Optional[User]:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Inactive user")

    return current_user

def get_current_active_authorized_user(request: Request, current_active_user: User = Security(get_current_active_user)) -> Optional[User]:
    username = current_active_user.Username
    path = request.state.path

    sub = username
    obj = path
    act = request.method.lower()

    print(sub, obj, act)

    if enforcer.enforce(sub, obj, act):
        return current_active_user
    else:
        raise HTTPException(status_code = HTTP_403_FORBIDDEN, detail="No permission")
