from pydantic import BaseModel, Field
from typing import List
import pypandoc
from enum import Enum

available_format = pypandoc.get_pandoc_formats()[1]

class ConvertTextParams(BaseModel):
    source: str = Field(None, description= 'Unicode string or bytes (see encoding)')
    to: str = Field(..., description= 'format into which the input should be convertedcan be one of {}'.format(pypandoc.get_pandoc_formats()[1]))
    format: str= Field(..., description='the format of the inputs; can be one of {}'.format(pypandoc.get_pandoc_formats()[1]))
    extra_args: List[str] = Field((), description='extra arguments (list of strings) to be passed to pandoc (Default value = ())')
    encoding: str = Field('utf-8', description="the encoding of the input bytes (Default value = 'utf-8')")
    filters: List[str] = Field(None, description="pandoc filters e.g. filters=['pandoc-citeproc']")

