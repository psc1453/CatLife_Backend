import uvicorn

if __name__ == "__main__":
    uvicorn.run('main:CatLife_Backend', host="0.0.0.0", port=228, reload=True)
