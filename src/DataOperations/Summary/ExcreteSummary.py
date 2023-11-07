from pathlib import Path

from fastapi import APIRouter

from lib.SQL.DB import DB
from lib.SQL.ViewOperations.ViewExcreteEveryday import ViewExcreteEveryday
from lib.Web.utils import table_to_dict

db = DB.from_yaml(Path('db_info.yml').resolve())  # Working directory is the project root
view_excrete = ViewExcreteEveryday(db)

excrete_summary_router = APIRouter(
    prefix='/excrete',
    tags=['Excrete Summary']
)


@excrete_summary_router.get('/get_full_excrete_summary')
async def get_full_excrete_summary():
    view = view_excrete.get_excrete_records_all()
    return table_to_dict(view)


@excrete_summary_router.get('/get_excrete_summary_by_date/{date}')
async def get_excrete_summary_by_date(date: str):
    view = view_excrete.get_excrete_records_by_date(date=date)
    return table_to_dict(view)


@excrete_summary_router.get('/get_excrete_summary_by_interval/{date_start}/{date_end}')
async def get_excrete_summary_by_interval(date_start: str, date_end: str):
    view = view_excrete.get_excrete_records_by_interval(date_start, date_end)
    return table_to_dict(view)
