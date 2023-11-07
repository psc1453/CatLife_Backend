from datetime import datetime

from pydantic import BaseModel, validator

from lib.SQL.TableOperations.TableStoolRecords import StoolStatus


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
