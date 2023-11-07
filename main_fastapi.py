from fastapi import FastAPI

from src.DataOperations import DataOperationsRouter

app = FastAPI()
app.include_router(DataOperationsRouter.table_router)
app.include_router(DataOperationsRouter.summary_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
