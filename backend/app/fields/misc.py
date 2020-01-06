from typing import Optional, List

from pydantic import BaseModel

class DataTable(BaseModel):
    headers: List[dict]
    items: List[dict]
