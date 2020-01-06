from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.responses import Response
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED

from app import crud
from app.fields.role import Role

router = APIRouter()


@router.get("/get_all_roles/", response_model=List[Role])
def get_all_roles():
    """
    Retrieve roles.
    """
    user_roles = crud.role.get_all_roles()
    return user_roles
