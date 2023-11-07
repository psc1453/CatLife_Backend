from pathlib import Path

from fastapi import APIRouter

from lib.SQL.DB import DB
from lib.SQL.ViewOperations.ViewDietEveryday import ViewDietEveryday
from lib.Web.utils import table_to_dict

db = DB.from_yaml(Path('db_info.yml').resolve())  # Working directory is the project root
view_diet = ViewDietEveryday(db)

diet_summary_router = APIRouter(
    prefix='/diet',
    tags=['Diet Summary']
)


@diet_summary_router.get('/get_full_diet_summary')
async def get_full_diet_summary():
    view = view_diet.get_diet_records_all()
    return table_to_dict(view)


@diet_summary_router.get('/get_diet_summary_by_date/{date}')
async def get_diet_summary_by_date(date: str):
    view = view_diet.get_diet_records_by_date(date=date)
    return table_to_dict(view)


@diet_summary_router.get('/get_diet_summary_by_interval/{date_start}/{date_end}')
async def get_diet_summary_by_interval(date_start: str, date_end: str):
    view = view_diet.get_diet_records_by_interval(date_start, date_end)
    return table_to_dict(view)
