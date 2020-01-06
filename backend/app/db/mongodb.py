from app.core.config import MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS

from pydantic import BaseModel, Field
from bson import ObjectId

class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)

class MyModel(BaseModel):
    id: ObjectIdStr = Field(..., alias="_id")
    class Config:
        allow_population_by_field_name=True
        dict_encoders = {str: lambda x: ObjectId(x) if ObjectId.is_valid(x) else x}


db_connect_dict_for_client = dict(
    host = MONGO_HOST,
    port = MONGO_PORT,
    username = MONGO_USER,
    password = MONGO_PASS
)

db_connection_dict_base = dict(**db_connect_dict_for_client, authentication_source='admin')