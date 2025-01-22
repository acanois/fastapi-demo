from datetime import datetime
from typing import List
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    username: str = Field()
    email: str = Field()
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    active: bool

class UserList(SQLModel):
    users: List[User]
