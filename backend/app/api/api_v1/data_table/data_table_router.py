
from fastapi import Depends, FastAPI, Header, HTTPException

from fastapi import APIRouter
from typing import Callable, List

from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

# from app.api.api_v1.endpoints import items, users

from app.api.api_v1.data_table import product, sales
from app.core.casbin_auth import CasbinRoute


router = APIRouter()

router.route_class = CasbinRoute


router.include_router(product.router, prefix="/product", tags=["product"])
router.include_router(sales.router, prefix="/sales", tags=["sales"])


