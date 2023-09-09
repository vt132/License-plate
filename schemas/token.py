import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    exp: datetime.datetime
