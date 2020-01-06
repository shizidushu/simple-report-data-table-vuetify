from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
import datetime
import time

from app.core.casbin_auth import CasbinRoute

from typing import List
from app.fields.misc import DataTable
from app.api.utils.prefetch import get_choices

import pandas as pd

router = APIRouter()
router.route_class = CasbinRoute


@router.get("/pass_input_meta/", summary="pass_input_meta", description="# Pass input meta to frontend to generate ui")
async def pass_input_meta(
        check: bool = Query(..., additionalProperties={"fieldType": "TCheckbox",
                                                            'label': "Checkbox"}),
        text: str = Query(..., additionalProperties={"fieldType": "TTextarea",
                                                            'rules': 'required',
                                                            'label': "文本输入框"}),
        title: List[str] = Query(..., additionalProperties={"fieldType": "TSelect",
                                                            'multiple': True,
                                                            'label': "Title",
                                                            'rules': 'required',
                                                            'items': ["", "Mr", "Ms", "Mx", "Dr", "Madam", "Lord"]}),
        title2: List[str] = Query(..., additionalProperties={"fieldType": "TAutocomplete",
                                                            'multiple': True,
                                                            'label': "Title2",
                                                            'rules': 'required',
                                                            'items': ["", "Mr", "Ms", "Mx", "博士", "女士", "Lord"]}),
        firstName: str = Query(None, additionalProperties={'fieldType': "TTextField",
                                                           'placeholder': "First Name",
                                                           'label': "First Name",
                                                           'rules': "max:10"}),
        Email: EmailStr = Query(..., additionalProperties={'fieldType': "TTextField",
                                                           'placeholder': "Email",
                                                           'label': "E-mail Address",
                                                           'rules': "required|email"}),
        age: int = Query(..., le=1000, additionalProperties={'fieldType': "TTextField",
                                                             'placeholder': "年龄",
                                                             'type': "number",
                                                             'label': "年龄",
                                                             'rules': "required|max_value:1000",
                                                             'counter': 10}),
        birthday: datetime.date = Query(..., additionalProperties={'fieldType': "TDatePicker",
                                                                   'label': "生日",
                                                                   'placeholder': '生日',
                                                                   'rules': 'required',
                                                                   'readonly': True,
                                                                   'menu': {'offset-y': True},
                                                                   'datePicker': {
                                                                       'first-day-of-week': '1'}
                                                                   }),
        bedtime: datetime.date = Query(..., additionalProperties={'fieldType': "TTimePicker",
                                                                   'label': "时间",
                                                                   'placeholder': '时间',
                                                                   'rules': 'required',
                                                                   'readonly': True,
                                                                   'menu': {'offset-y': True},
                                                                   'timePicker': {
                                                                       'format': 'ampm'}
                                                                   })):
    return {'title': title, 'firstName': firstName, 'Email': Email, 'age': age}


@router.get("/order_amount2/", response_model=DataTable, summary="create echo", description="it is order_amount2")
async def read_order_amount(test: str = Query(None, max_length=50, additionalProperties={
    'type': 'select',
            'label': 'Skills',
            'model': 'skills',
            'values': get_choices()
})):
    df = pd.read_excel("order2.xlsx")
    headers = [
        { 'text': "年", 'value': "年" },
        { 'text': "订单总金额USD", 'value': "订单总金额USD" },
        { 'text': "订单号", 'value': "订单号" }
      ]
    time.sleep(15)
    return DataTable(headers= headers, items = df.to_dict('records'))
