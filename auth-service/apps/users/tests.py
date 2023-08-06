# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
import jwt
import pytest

from apps.settings import get_settings
from apps.users.models import User
from apps.users.schemas import User_Pydantic

settings = get_settings()


async def get_user_with_token(*args, **kwargs) -> tuple[User_Pydantic, str]:
    user = await User.create(**kwargs)
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(jsonable_encoder(user_obj.dict()), settings.SECRET_KEY)
    return user, token


@pytest.mark.anyio
async def test_create_user(client: AsyncClient):
    response = await client.post("/auth/signup", json={"email": "admin@gmail.com", "password": "Test1234"})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "admin@gmail.com"
    assert "id" in data
    user_id = data["id"]

    user_obj = await User.get(id=user_id)
    assert str(user_obj.id) == user_id


@pytest.mark.anyio
async def test_retreieve_user(client: AsyncClient):
    user, token = await get_user_with_token(
        **{
            "email": "admin1@test.com",
            "password": "Test1234",
            "first_name": "Test",
            "last_name": "User1",
            "status": "ACTIVE"
        }
    )
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    response = await client.get(f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code, 200
    data = response.json()
    user_id = data.get("id")
    assert data.get("email") == "admin1@test.com"

    user_obj = await User.get(id=user_id)
    assert user_obj.id == user.id
