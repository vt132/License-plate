# This file is for openAPI docs input

from pydantic import BaseModel


# Create the Pydantic models
class LicensePlateBase(BaseModel):
    number: str
    wanted: bool


class LicensePlateCreate(LicensePlateBase):
    pass


class LicensePlateInDB(LicensePlateBase):
    id: int
