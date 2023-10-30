from datetime import datetime

from pydantic import BaseModel, validator

from lib.SQL.TableOperations.TableUrineRecords import UrineStatus


class UrineRecordModel(BaseModel):
    urine_timestamp: str
    urine_status: str = 'normal'
    urine_comment: str = None

    @validator('urine_timestamp')
    def is_valid_date(cls, input_date):
        try:
            datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid date string, only support format like \"2023-10-27 00:10:00\"!")
        return input_date

    @validator('urine_status')
    def is_valid_weight(cls, input_status):
        if input_status in [s.name for s in UrineStatus]:
            return input_status
        else:
            raise ValueError('Not a valid urine status')
