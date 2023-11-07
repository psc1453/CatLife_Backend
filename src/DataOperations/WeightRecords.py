from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, validator

from lib.SQL.DB import DB
from lib.SQL.TableOperations.TableWeightRecords import TableWeightRecords
from lib.Web.utils import table_to_dict


class WeightRecordModel(BaseModel):
    record_date: str
    weight: float

    @validator('record_date')
    def is_valid_date(cls, input_date):
        try:
            datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date string, only support format like \"2023-10-27\"!")
        return input_date

    @validator('weight')
    def is_valid_weight(cls, input_weight):
        if input_weight > 0:
            return input_weight
        else:
            raise ValueError('Weight should be positive!')


db = DB.from_yaml(Path('db_info.yml').resolve())  # Working directory is the project root
table_weight = TableWeightRecords(db)

weight_router = APIRouter(
    prefix='/weight',
    tags=['Weight Records']
)


@weight_router.post('/add_record')
async def add_record(record: WeightRecordModel):
    record_dict = record.dict()
    try:
        table_weight.insert_record(record_dict)
    except Exception as error:
        print(error)
        message = {"message": str(error)}
        return message
    else:
        status_dict = {"inserted": record_dict, "message": "ok"}
        return status_dict


@weight_router.get('/get_full_table')
async def get_full_table():
    table = table_weight.get_weight_records_all()
    return table_to_dict(table)


@weight_router.get('/get_record_by_date/{date}')
async def get_weight_record_by_date(date: str):
    table = table_weight.get_weight_record_by_date(date=date)
    return table_to_dict(table)


@weight_router.get('/get_records_by_interval/{date_start}/{date_end}')
async def get_records_by_interval(date_start: str, date_end: str):
    table = table_weight.get_weight_records_by_interval(date_start, date_end)
    return table_to_dict(table)
