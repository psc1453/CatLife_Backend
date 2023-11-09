from fastapi import FastAPI

from src.DataOperations import DataOperationsRouter

CatLife_Backend = FastAPI()
CatLife_Backend.include_router(DataOperationsRouter.table_router)
CatLife_Backend.include_router(DataOperationsRouter.summary_router)


@CatLife_Backend.get("/")
async def root():
    return {"message": "Hello World"}


@CatLife_Backend.post("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
