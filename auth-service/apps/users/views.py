import json
from typing import Annotated, List
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
import jwt
from passlib.hash import bcrypt
from tortoise.exceptions import IntegrityError, DoesNotExist

from apps.users import InterestChoices
from apps.users.schemas import (
    ChangePassowrd,
    SignIn,
    User,
    User_Pydantic,
    UserIn_Pydantic,
    UserToken,
    UserToken_Pydantic,
)
from apps.core.mail import send_mail
from apps.core.security import (
    create_verification_token,
    validate_token,
    authenticate_user,
    get_current_user,
    settings
)
from apps.users.signals import generate_and_save_user_data_for_redis_hash_model

router = InferringRouter()


@cbv(router)
class UserViews:

    @router.get("/users/interests-choices", status_code=status.HTTP_200_OK, tags=["user"])
    async def get_available_interests_choices(self):
        return JSONResponse(status_code=status.HTTP_200_OK, content=InterestChoices.values())

    @router.post("/users/activate", tags=["user"])
    async def activate_user(self, activation_token):
        result = await validate_token(activation_token)
        if result.get("status_code") == status.HTTP_200_OK:
            await User.get(id=result.get("user").update(is_active=True))
            return await User_Pydantic.from_queryset_single(User.get(id=result.get("user")))
        return result

    @router.get("/users", response_model=List[User_Pydantic], tags=["user"])
    async def get_users(self, current_user: Annotated[User, Depends(get_current_user)]):
        if current_user:
            return await User_Pydantic.from_queryset(User.all())
        else:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN)

    @router.get("/users/me", response_model=User_Pydantic, tags=["user"])
    async def get_session_user(self, user: User_Pydantic = Depends(get_current_user)):
        return user

    @router.get("/users/{user_id}", response_model=User_Pydantic, tags=["user"])
    async def retrieve_user(self, user_id: UUID, current_user: Annotated[User, Depends(get_current_user)]):
        return await User_Pydantic.from_queryset_single(User.get(id=user_id))

    @router.put("/users/{user_id}", response_model=User_Pydantic, tags=["user"])
    async def update_user(
        self, user_id: int, user: UserIn_Pydantic, current_user: Annotated[User, Depends(get_current_user)]
    ):
        if current_user.id == user_id:
            user.password_hash = bcrypt.hash(user.password_hash)
            await User.get(id=user_id).update(**user.dict(exclude_unset=True))
            return await User_Pydantic.from_queryset_single(User.get(id=user_id))
        else:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN)

    @router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["user"])
    async def delete_user(self, user_id: UUID, current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.id == user_id:
            await User.filter(id=user_id).delete()
            return {}
        else:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN)

    @router.post("/users/{user_id}/connect", response_model=User_Pydantic, tags=["user"])
    async def add_user_connection(self, user_id: UUID, current_user: User_Pydantic = Depends(get_current_user)):
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not self connect"
            )
        try:
            target_user = await User.get(id=user_id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target user not found"
            )
        else:
            user = await User.get(id=current_user.id)
            await user.connections.add(target_user)
            await generate_and_save_user_data_for_redis_hash_model(user)
            await generate_and_save_user_data_for_redis_hash_model(target_user)
        return await User_Pydantic.from_tortoise_orm(user)

    @router.delete(
            "/users/{user_id}/disconnect", status_code=status.HTTP_204_NO_CONTENT, response_model=None, tags=["user"]
    )
    async def remove_user_connection(self, user_id: UUID, current_user: User_Pydantic = Depends(get_current_user)):
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not self disconnect"
            )
        try:
            target_user = await User.get(id=user_id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target user not found"
            )
        else:
            user = await User.get(id=current_user.id)
            await user.connections.remove(target_user)
            await generate_and_save_user_data_for_redis_hash_model(user)
            await generate_and_save_user_data_for_redis_hash_model(target_user)
        return {}

    @router.get("/users/me/connections", response_model=List[User_Pydantic], tags=["user"])
    async def user_connections(self, current_user: User_Pydantic = Depends(get_current_user)):
        user = await User.get(id=current_user.id)
        return await User_Pydantic.from_queryset(
            User.filter(id__in=await user.connections.all().values_list("id", flat=True))
        )


@cbv(router)
class AuthViews:

    @router.post("/auth/signup", response_model=User_Pydantic, status_code=status.HTTP_201_CREATED, tags=["auth"])
    async def sign_up(self, user: UserIn_Pydantic):
        user_data = user.dict(exclude_unset=True)
        user_data.update({"password": bcrypt.hash(user_data.pop("password"))})
        if set(user.interests).difference(set(InterestChoices.values())):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Should be from valid interest choices"
            )
        try:
            user_obj = await User.create(**user_data)
        except IntegrityError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
        else:
            verification_token = await create_verification_token(user_obj)
            # send_mail(user_obj.email, "Activate Account", f'<strong>{verification_token.token}</strong>')
        return await User_Pydantic.from_tortoise_orm(user_obj)

    @router.post("/auth/signin", status_code=status.HTTP_200_OK, tags=["auth"])
    async def sign_in(self, sign_data: SignIn):
        user = await authenticate_user(sign_data.email, sign_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong username or password")
        user_obj = await User_Pydantic.from_tortoise_orm(user)
        token = jwt.encode(jsonable_encoder(user_obj.dict()), settings.SECRET_KEY)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": token, "token_type": "bearer"})

    @router.post("/auth/forgot-password", tags=["auth"])
    async def forgot_password(self, email: str):
        user = await User.get(email=email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        try:
            user_token_obj = await create_verification_token(user)
            # send_mail(email, "VanUse - Reset Password", f'<strong>{user_token_obj.token}</strong>')
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Oops Something Went wrong {e.message}"
            )
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user_token_obj))

    @router.post("/auth/change-password", tags=["auth"])
    async def change_password(
        self, current_user: Annotated[User, Depends(get_current_user, use_cache=False)], data: ChangePassowrd
    ):
        user = await User.get(id=current_user.id)
        if not user.verify_password(data.current_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password not matching")
        if data.new_password != data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and confirm password missmatched"
            )
        user.password = bcrypt.hash(data.new_password)
        await user.save()

        user_obj = await User_Pydantic.from_tortoise_orm(user)
        token = jwt.encode(jsonable_encoder(user_obj.dict()), settings.SECRET_KEY)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": token, "token_type": "bearer"})

    @router.post("/auth/reset-password", tags=["auth"])
    async def reset_password(self, reset_token: str, password: str, confirmed_password: str):
        result = await validate_token(reset_token)
        if result["status_code"] == status.HTTP_200_OK and password == confirmed_password:
            await User.get(id=result['user']).update(password_hash=bcrypt.hash(password))
            return await User_Pydantic.from_queryset_single(User.get(id=result["user"]))
        return result


@cbv(router)
class TokenViews:
    @router.post("/auth/token", tags=["auth"])
    async def generate_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        user_obj = await User_Pydantic.from_tortoise_orm(user)
        token = jwt.encode(jsonable_encoder(user_obj.dict()), settings.SECRET_KEY)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": token, "token_type": "bearer"})

    @router.get("/auth/all-tokens", response_model=List[UserToken_Pydantic], tags=["auth"])
    async def get_tokens(self, current_user: Annotated[User, Depends(get_current_user)]):
        return await UserToken_Pydantic.from_queryset(UserToken.filter(user=current_user))

    @router.get("/auth/verify-token", tags=["auth"], status_code=status.HTTP_200_OK)
    async def verify_token(self, user: User_Pydantic = Depends(get_current_user)):
        user_obj = await User.get(id=user.id)
        total_connections = await user_obj.connections.all().count()
        user_dict = json.loads(user.json())
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={**user_dict, "total_connections": total_connections}
        )
