from pydantic import BaseModel, Field
from typing import List


class ConferenceModel(BaseModel):
    name: str
    articles: List[str] = []
    date_of_conference: List[str]
