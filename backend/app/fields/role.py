from typing import Optional, List

from pydantic import BaseModel
from app.fields.user import UserBase, Permission



class Role(BaseModel):
    name: str
    users: List[UserBase]
    permissions: List[Permission]