from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    active: bool
