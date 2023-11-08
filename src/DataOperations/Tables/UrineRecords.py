from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, validator

from lib.SQL.DB import DB
from lib.SQL.TableOperations.TableUrineRecords import UrineStatus, TableUrineRecords
from lib.Web.utils import table_to_dict


class UrineRecordModel(BaseModel):
    urine_timestamp: str
    urine_status: str = 'normal'
    urine_comment: str = None

    @validator('urine_timestamp')
    def is_valid_timestamp(cls, input_timestamp):
        if input_timestamp is not None:
            try:
                datetime.strptime(input_timestamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError("Invalid date string, only support format like \"2023-10-27 00:10:00\"!")
            return input_timestamp
        else:
            return input_timestamp

    @validator('urine_status')
    def is_valid_status(cls, input_status):
        if input_status in [s.name for s in UrineStatus]:
            return input_status
        else:
            raise ValueError('Not a valid urine status')


db = DB.from_yaml(Path('db_info.yml').resolve())  # Working directory is the project root
table_urine = TableUrineRecords(db)

urine_router = APIRouter(
    prefix='/urine',
    tags=['Urine Records']
)


@urine_router.post('/add_urine_record')
async def add_urine_record(record: UrineRecordModel):
    record_dict = record.dict()
    try:
        table_urine.insert_record(record_dict)
    except Exception as error:
        print(error)
        message = {"message": str(error)}
        return message
    else:
        status_dict = {"inserted": record_dict, "message": "ok"}
        return status_dict


@urine_router.get('/get_full_urine_table')
async def get_full_urine_table():
    table = table_urine.get_urine_records_all()
    return table_to_dict(table)


@urine_router.get('/get_urine_record_by_id/{urine_id}')
async def get_urine_record_by_id(urine_id: int):
    table = table_urine.get_urine_record_by_id(urine_id=urine_id)
    return table_to_dict(table)


@urine_router.get('/get_urine_records_by_date/{date}')
async def get_urine_records_by_date(date: str):
    table = table_urine.get_urine_records_by_date(date=date)
    return table_to_dict(table)


@urine_router.get('/get_urine_records_by_interval/{date_start}/{date_end}')
async def get_urine_records_by_interval(date_start: str, date_end: str):
    table = table_urine.get_urine_records_by_interval(date_start, date_end)
    return table_to_dict(table)


@urine_router.delete('/delete_urine_record_by_id/{urine_id}')
async def delete_urine_record_by_id(urine_id: int):
    try:
        table_urine.delete_urine_record_by_id(urine_id)
    except Exception as error:
        print(error)
        message = {"message": str(error)}
        return message
    else:
        status_dict = {"deleted": urine_id, "message": "ok"}
        return status_dict


@urine_router.put('/update_urine_record_by_id_with_dict/{urine_id}')
async def update_urine_record_by_date_with_dict(urine_id: int, update_dict: dict):
    try:
        table_urine.update_urine_record_by_id_with_dict(urine_id, update_dict)
    except Exception as error:
        print(error)
        message = {"message": str(error)}
        return message
    else:
        status_dict = {"updated": {"urine_id": urine_id, "value": update_dict}, "message": "ok"}
        return status_dict
