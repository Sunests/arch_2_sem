import datetime
from pydantic import BaseModel


class Article(BaseModel):
    title: str
    text: str
    UDK: str
    date_of_load: datetime.datetime
    presentation_date: datetime.datetime
