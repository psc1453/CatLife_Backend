from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, validator

from lib.SQL.DB import DB
from lib.SQL.TableOperations.TableStoolRecords import StoolStatus, TableStoolRecords
from lib.Web.utils import table_to_dict


class StoolRecordModel(BaseModel):
    stool_timestamp: str
    stool_status: str = 'normal'
    stool_comment: str = None

    @validator('stool_timestamp')
    def is_valid_timestamp(cls, input_date):
        try:
            datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid date string, only support format like \"2023-10-27 00:10:00\"!")
        return input_date

    @validator('stool_status')
    def is_valid_status(cls, input_status):
        if input_status in [s.name for s in StoolStatus]:
            return input_status
        else:
            raise ValueError('Not a valid stool status')


db = DB.from_yaml(Path('db_info.yml').resolve())  # Working directory is the project root
table_stool = TableStoolRecords(db)

stool_router = APIRouter(
    prefix='/stool',
    tags=['Stool Records']
)


@stool_router.post('/add_stool_record')
async def add_stool_record(record: StoolRecordModel):
    record_dict = record.dict()
    try:
        table_stool.insert_record(record_dict)
    except Exception as error:
        print(error)
        message = {"message": str(error)}
        return message
    else:
        status_dict = {"inserted": record_dict, "message": "ok"}
        return status_dict


@stool_router.get('/get_full_stool_table')
async def get_full_stool_table():
    table = table_stool.get_stool_records_all()
    return table_to_dict(table)


@stool_router.get('/get_stool_record_by_date/{date}')
async def get_stool_record_by_date(date: str):
    table = table_stool.get_stool_records_by_date(date=date)
    return table_to_dict(table)


@stool_router.get('/get_stool_records_by_interval/{date_start}/{date_end}')
async def get_stool_records_by_interval(date_start: str, date_end: str):
    table = table_stool.get_stool_records_by_interval(date_start, date_end)
    return table_to_dict(table)
