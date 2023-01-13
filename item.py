from pydantic import BaseModel
from typing import List, Union

class movieItem(BaseModel):
    title: str
    runtime: int
    release_date: str
    collection: Union[int, None] = None
    genres: List[int]
    overview: str
    actors: List[int]

class collectionItem(BaseModel):
    name: str
