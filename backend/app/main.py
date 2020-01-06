from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from mongoengine import connect, disconnect

from app.api.api_v1.api import api_router
from app.core import config
from app.db.mongodb import db_connection_dict_base
from app.core.config import (
    API_V1_STR, PROJECT_NAME, MONGO_DEFAULT_DB, MONGO_FS_DB)
from app.core.casbin_auth import CasbinRoute, extract_path_info_of_tag
from app.core.permission import enforcer


app = FastAPI(title=PROJECT_NAME)
app.router.route_class = CasbinRoute

# CORS
origins = []

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
def startup():
    connect(**db_connection_dict_base, db=MONGO_DEFAULT_DB)
    connect(**db_connection_dict_base, db=MONGO_FS_DB, alias=MONGO_FS_DB)
    connect(**db_connection_dict_base, db='fastapi', alias='fastapi')

    data_table_paths = extract_path_info_of_tag(app, 'dataTable')

    # add policy for all table paths
    for data_table_path in data_table_paths:
        enforcer.add_policy(data_table_path['tags'], data_table_path['path'], data_table_path['method'] )
        enforcer.add_policy('role_root', data_table_path['path'], data_table_path['method'] )

    enforcer.add_grouping_policy("username", "dataTable_product_ungrouped")
    enforcer.add_grouping_policy("username", "role_root")


@app.on_event("shutdown")
def shutdown():
    disconnect(alias=MONGO_FS_DB)
    disconnect(alias='fastapi')



app.include_router(api_router, prefix=API_V1_STR)
