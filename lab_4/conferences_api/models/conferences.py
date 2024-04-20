from pydantic import BaseModel, Field
from typing import List


class ConferenceModel(BaseModel):
    name: str
    articles: List[str] = []
    date_of_conference: List[str]


class ConferenceUpdateModel(BaseModel):
    name: str | None = None
    articles: List[str] | None = None
    date_of_conference: List[str] | None = None
