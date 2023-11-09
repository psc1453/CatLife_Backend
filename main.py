import os

import uvicorn

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    uvicorn.run('main_fastapi:CatLife_Backend', host="0.0.0.0", port=228, reload=True)
