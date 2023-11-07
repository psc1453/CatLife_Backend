from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from lib.SQL.DB import DB
from lib.SQL.TableOperations.TableFoodList import TableFoodList
from lib.Web.utils import table_to_dict


class FoodRecordModel(BaseModel):
    food_brand: str = None
    food_name: str
    food_category: str
    food_unit: str


db = DB.from_yaml(Path('db_info.yml').resolve())  # Working directory is the project root
table_food = TableFoodList(db)

food_router = APIRouter(
    prefix='/food',
    tags=['Food List']
)


@food_router.post('/add_food_record')
async def add_food_record(record: FoodRecordModel):
    record_dict = record.dict()
    try:
        table_food.insert_record(record_dict)
    except Exception as error:
        print(error)
        message = {"message": str(error)}
        return message
    else:
        status_dict = {"inserted": record_dict, "message": "ok"}
        return status_dict


@food_router.get('/get_full_food_table')
async def get_full_food_table():
    table = table_food.get_food_records_all()
    return table_to_dict(table)


@food_router.get('/get_full_food_products_table')
async def get_full_food_products_table():
    table = table_food.get_food_products_all()
    return table_to_dict(table)


@food_router.get('/get_food_record_by_id/{food_id}')
async def get_food_record_by_id(food_id: int):
    table = table_food.get_food_record_by_id(food_id=food_id)
    return table_to_dict(table)


@food_router.get('/fine_food_records_by_name/{food_name}')
async def fine_food_records_by_name(food_name: str):
    table = table_food.find_food_records_by_name(name=food_name)
    return table_to_dict(table)
