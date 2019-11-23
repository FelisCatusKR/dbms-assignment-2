from typing import List
from pydantic import BaseModel, Schema


class UserBase(BaseModel):
    name: str = Schema(None, min_length=1)
    phone_number: str = Schema(None, regex="010\d\d\d\d\d\d\d\d")


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class SearchResult(BaseModel):
    first_name: str
    first_name_number: int
    number: int
    user_list: List[User]
