from datetime import datetime

from pydantic import BaseModel, validator


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
