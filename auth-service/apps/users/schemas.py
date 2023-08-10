from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from apps.users.models import User, UserToken


class ChangePassowrd(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class SignIn(BaseModel):
    email: str
    password: str


class UserConnection(BaseModel):
    user_id: str


User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password",))
UserIn_Pydantic = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True, exclude=("is_verified", "status", "rating", "connection")
)

UserToken_Pydantic = pydantic_model_creator(UserToken, name="UserToken")
UserTokenIn_Pydantic = pydantic_model_creator(UserToken, name="UserTokenIn", exclude_readonly=True)
