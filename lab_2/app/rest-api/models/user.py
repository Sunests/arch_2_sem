from pydantic import BaseModel


class UserModel(BaseModel):
    user_name: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    affiliation: str | None = None
    password: str | None = None
