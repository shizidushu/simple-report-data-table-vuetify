from pathlib import Path
import casbin
from app.db.mongodb import db_connection_dict_base
from app.db.casbin_mongoengine_adapter import Adapter


model_file_path = Path(__file__).parent / "casbin_model.conf"
model_file_path = str(model_file_path.absolute())

adapter = Adapter(db='casbin', **db_connection_dict_base)

enforcer = casbin.Enforcer(model_file_path, adapter, True)