from fastapi import Depends, FastAPI, Header, HTTPException

from fastapi import APIRouter

from app.core.casbin_auth import CasbinRoute

router = APIRouter()
router.route_class = CasbinRoute


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.get("/items/", summary= "create items", description="it is 1")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@router.get("/items2/", summary= "create items2", description="it is 2")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]