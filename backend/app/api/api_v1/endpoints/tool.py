from fastapi import APIRouter, Body
import pypandoc

from app.fields.tools import ConvertTextParams

router = APIRouter()


@router.post("/convert_text/")
async def convert_text(params: ConvertTextParams = Body(..., example = {"source": "#some title", "to": "html", "format": "md"})) -> str:
    output = pypandoc.convert_text(**params.dict())
    return output
