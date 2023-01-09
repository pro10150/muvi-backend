from typing import Union
from fastapi import FastAPI

#init app
app = FastAPI()

#setup

#api
@app.get("/")
def read_root():
    return {"Hello": "Word"}

@app.get("/item/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}