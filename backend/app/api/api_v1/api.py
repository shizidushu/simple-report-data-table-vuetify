from fastapi import Depends, FastAPI, Header, HTTPException

from fastapi import APIRouter

# from app.api.api_v1.endpoints import items, users
from app.api.utils.security import get_current_active_user, get_current_active_authorized_user

from app.api.api_v1.endpoints import login, user, perm, tool, role
from app.api.api_v1.data_table import data_table_router

from app.core.casbin_auth import CasbinRoute


api_router = APIRouter()
api_router.route_class = CasbinRoute

api_router.include_router(role.router, prefix="/role", tags=["role"])
api_router.include_router(tool.router, prefix="/tool", tags=["tool"])
api_router.include_router(login.router, prefix="/login", tags=["login"])

api_router.include_router(user.router, prefix="/user", dependencies=[Depends(get_current_active_user)],  tags=["user"])

api_router.include_router(perm.router, prefix="/perm", dependencies=[Depends(get_current_active_user)],  tags=["permission"])

api_router.include_router(data_table_router.router, prefix="/data_table", dependencies=[Depends(get_current_active_authorized_user)], tags=["dataTable"])