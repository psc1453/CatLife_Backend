from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, validator

from lib.SQL.DB import DB
from lib.SQL.TableOperations.TableDietRecords import TableDietRecords
from lib.Web.utils import table_to_dict


class DietRecordModel(BaseModel):
    food_id: int
    food_quantity: int
    diet_timestamp: str = 'DEFAULT'

    @validator('diet_timestamp')
    def is_valid_timestamp(cls, input_timestamp):
        if input_timestamp is not None:
            try:
                datetime.strptime(input_timestamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError("Invalid date string, only support format like \"2023-10-27 00:10:00\"!")
            return input_timestamp
        else:
            return input_timestamp

    @validator('food_quantity')
    def is_valid_quantity(cls, input_quantity):
        if input_quantity > 0:
            return input_quantity
        else:
            raise ValueError('Quantity should be positive!')


db = DB.from_yaml(Path('db_info.yml').resolve())  # Working directory is the project root
table_diet = TableDietRecords(db)

diet_router = APIRouter(
    prefix='/diet',
    tags=['Diet Record']
)


@diet_router.post('/add_diet_record')
async def add_diet_record(record: DietRecordModel):
    record_dict = record.dict()
    try:
        table_diet.insert_record(record_dict)
    except Exception as error:
        print(error)
        message = {"message": str(error)}
        return message
    else:
        status_dict = {"inserted": record_dict, "message": "ok"}
        return status_dict


@diet_router.get('/get_full_diet_table')
async def get_full_diet_table():
    table = table_diet.get_diet_records_all()
    return table_to_dict(table)


@diet_router.get('/get_diet_record_by_id/{diet_id}')
async def get_diet_record_by_id(diet_id: int):
    table = table_diet.get_diet_record_by_id(diet_id=diet_id)
    return table_to_dict(table)


@diet_router.get('/get_diet_records_by_date/{date}')
async def get_diet_records_by_date(date: str):
    table = table_diet.get_diet_records_by_date(date=date)
    return table_to_dict(table)


@diet_router.get('/get_diet_records_by_interval/{date_start}/{date_end}')
async def get_diet_records_by_interval(date_start: str, date_end: str):
    table = table_diet.get_diet_records_by_interval(date_start, date_end)
    return table_to_dict(table)


@diet_router.delete('/delete_diet_record_by_id/{diet_id}')
async def delete_diet_record_by_id(diet_id: int):
    try:
        table_diet.delete_diet_record_by_id(diet_id)
    except Exception as error:
        print(error)
        message = {"message": str(error)}
        return message
    else:
        status_dict = {"deleted": diet_id, "message": "ok"}
        return status_dict


@diet_router.put('/update_diet_record_by_id_with_dict/{diet_id}')
async def update_diet_record_by_date_with_dict(diet_id: int, update_dict: dict):
    try:
        table_diet.update_diet_record_by_id_with_dict(diet_id, update_dict)
    except Exception as error:
        print(error)
        message = {"message": str(error)}
        return message
    else:
        status_dict = {"updated": {"diet_id": diet_id, "value": update_dict}, "message": "ok"}
        return status_dict
