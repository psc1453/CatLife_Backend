from fastapi import APIRouter

from src.DataOperations.Summary import DietSummary
from src.DataOperations.Tables import WeightRecords, FoodRecords, DietRecords, UrineRecords, StoolRecords

table_router = APIRouter(
    prefix='/tables',
    tags=['Tables']
)

table_router.include_router(WeightRecords.weight_router)
table_router.include_router(FoodRecords.food_router)
table_router.include_router(DietRecords.diet_router)
table_router.include_router(UrineRecords.urine_router)
table_router.include_router(StoolRecords.stool_router)

summary_router = APIRouter(
    prefix='/summaries',
    tags=['Summaries']
)

summary_router.include_router(DietSummary.diet_summary_router)
