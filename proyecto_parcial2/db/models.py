from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: str = Field(unique=True, index=True)
    hashed_password: str


class UserCreate(SQLModel):
    name: str
    username: str
    password: str


class UserPublic(SQLModel):
    id: int
    name: str
    username: str
    hashed_password: str