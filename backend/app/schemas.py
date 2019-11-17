from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    phone_number: str


class User(UserBase):
    id: int
    name: str
    phone_number: str

    class Config:
        orm_mode = True
