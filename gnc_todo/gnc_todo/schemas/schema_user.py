from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    username: str
    password: str


class UserSchemaPublic(BaseModel):
    id: int
    username: str
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserSchemaList(BaseModel):
    users: list[UserSchemaPublic]
