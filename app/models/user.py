from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    username: str = Field()
    email: str = Field()
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    active: bool
