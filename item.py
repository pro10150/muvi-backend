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
    image: Union[str, None] = None

class collectionItem(BaseModel):
    name: str

class actorItem(BaseModel):
    firstName: str
    middleName: Union[str, None] = None
    familyName: str
    birthday: str
    image: Union[str, None] = None
    gender: int

class castItem(BaseModel):
    movie_id: int
    actor_id: int
