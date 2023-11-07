from datetime import datetime

from pydantic import BaseModel, validator


class DietRecordModel(BaseModel):
    food_id: int
    food_quantity: int
    diet_timestamp: str

    @validator('diet_timestamp')
    def is_valid_timestamp(cls, input_date):
        try:
            datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid date string, only support format like \"2023-10-27 00:10:00\"!")
        return input_date

    @validator('food_quantity')
    def is_valid_quantity(cls, input_quantity):
        if input_quantity > 0:
            return input_quantity
        else:
            raise ValueError('Quantity should be positive!')
