from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    phone_number: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class SearchResult(BaseModel):
    first_name: str
    first_name_number: int
    number: int
    user_list: List[User]
