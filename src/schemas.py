# schemas.py
# 프론트엔드와의 통신에 사용할 데이터의 형식을 지정해주는 모듈

from typing import List

from pydantic import BaseModel, Schema


class UserBase(BaseModel):
    name: str = Schema(None, min_length=1)
    phone: str = Schema(None, regex="010\d\d\d\d\d\d\d\d")


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class SearchResult(BaseModel):
    # 파싱한 쿼리의 성
    first_name: str
    # 파싱한 쿼리의 성과 같은 성을 가진 사람의 수
    first_name_number: int
    # 파싱한 쿼리와 이름의 앞부분이 일치하는 사람의 수
    number: int
    # 파싱한 쿼리와 이름의 앞부분이 일치하는 사람의 목록
    user_list: List[User]


class DeleteResult(BaseModel):
    result: bool = False


class Message(BaseModel):
    detail: str = "User not found"
