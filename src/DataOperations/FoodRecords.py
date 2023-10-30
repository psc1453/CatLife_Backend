from pydantic import BaseModel


class FoodRecordModel(BaseModel):
    food_brand: str = None
    food_name: str
    food_category: str
    food_unit: str
