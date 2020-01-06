from typing import Optional, List

from pydantic import BaseModel


class UserBase(BaseModel):
    ID: int
    Username: str
    IsLock: bool

    class Config:
        orm_mode = True

class Permission(BaseModel):
    sub: str = None
    obj: str = None
    act: str = None

class UserPerm(BaseModel):
    role_names: List[str] = None
    implicit_roles: List[str] = None
    permissions: List[Permission] = None
    implicit_permissions: List[Permission] = None

class User(UserPerm, UserBase):
    pass

class UserInDB(UserBase):
    Password: Optional[str] = None

class UserCreate(UserInDB):
    pass

class UserUpdate(UserInDB):
    pass

