from pydantic import BaseModel


class Toilet(BaseModel):
    toilet_id: int
    status: bool
    time_in: int
