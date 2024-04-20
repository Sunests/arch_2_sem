from pydantic import BaseModel


class UserModel(BaseModel):
    user_name: str | None
    first_name: str | None
    second_name: str | None
    affiliation: str | None
    password: str | None
