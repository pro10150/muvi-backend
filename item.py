from pydantic import BaseModel
from typing import List, Union

class movieItem(BaseModel):
    title: str
    runtime: int
    release_date: str
    collection: Union[int, None] = None
    overview: str
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
    character: str
    actor_id: int
    order: int

class movieGenreItem(BaseModel):
    movie_id: int
    genre_id: int

class loginItem(BaseModel):
    user: str
    password: str
