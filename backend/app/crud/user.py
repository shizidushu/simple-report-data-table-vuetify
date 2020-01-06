from typing import List, Optional
from app.mongodb_models.user import User as DBUser
from fastapi.encoders import jsonable_encoder

from app.fields.user import UserBase, UserCreate, UserUpdate
from app.core.security import verify_password, get_password_hash
from app.core.permission import enforcer

from app.fields.user import UserBase, User, UserPerm, Permission


def get_user_role_perm(username: str) -> UserPerm:
    role_names = enforcer.get_roles_for_user(username)
    implicit_roles = enforcer.get_implicit_roles_for_user(username)
    permissions = enforcer.get_permissions_for_user(username)
    permissions = [dict(zip(['sub', 'obj', 'act'], perm))
                   for perm in permissions]
    permissions = [Permission(**perm) for perm in permissions]

    implicit_permissions = enforcer.get_implicit_permissions_for_user(username)
    implicit_permissions = [dict(zip(['sub', 'obj', 'act'], perm))
                            for perm in implicit_permissions]
    implicit_permissions = [Permission(**perm) for perm in implicit_permissions]

    user_perm = UserPerm(role_names=role_names,
                         implicit_roles=implicit_roles,
                         permissions=permissions,
                         implicit_permissions=implicit_permissions)
    return user_perm


def get_db_user(username: str) -> Optional[DBUser]:
    db_user = DBUser.objects(Username=username).first()
    return db_user


def get_user_base(username: str) -> Optional[UserBase]:
    db_user = get_db_user(username)
    user_base = UserBase(ID=db_user.ID,
                         Username=db_user.Username,
                         IsLock=db_user.IsLock)
    return user_base


def get_user(username: str) -> User:
    # get role and permission
    user_perm = get_user_role_perm(username)

    # get basic user information
    user = get_user_base(username)

    # combine data
    user = User(**user.dict(), **user_perm.dict())

    return user


def authenticate(username: str, password: str) -> Optional[DBUser]:
    user = get_db_user(username)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.Password):
        return None
    return user


def is_active(user: User) -> bool:
    return not user.IsLock


def get_multi(skip=None, limit=None) -> List[Optional[User]]:
    slicer = slice(skip, limit, None)
    db_users = DBUser.objects[slicer]
    users_base = [UserBase(ID=db_user.ID, Username=db_user.Username, IsLock=db_user.IsLock) for db_user in db_users]
    users = [User(**user_base.dict(), **get_user_role_perm(user_base.Username).dict())
             for user_base in users_base]
    return [i for i in users]


def create(user_in: UserCreate) -> DBUser:
    user = DBUser(**user_in.dict(skip_defaults=True))
    user.save()
    return user


def update(user: DBUser, user_in: UserUpdate) -> DBUser:

    user_data = user
    update_data = user_in.dict(skip_defaults=True)
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    # the password passed in is already encrypted
    # so comment the following
    # if user_in.password:
    #     passwordhash = get_password_hash(user_in.password)
    #     user.hashed_password = passwordhash
    user.save()
    return user
