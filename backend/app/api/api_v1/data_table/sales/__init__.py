
from fastapi import APIRouter
from app.core.casbin_auth import CasbinRoute
from . import ungrouped


router = APIRouter()
router.route_class = CasbinRoute

router.include_router(
    ungrouped.router, prefix="/ungrouped", tags=['ungrouped'])
