import copy
import uuid
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import jwt
from tortoise import timezone

from apps.settings import get_settings
from apps.users.models import User, UserToken
from apps.users.schemas import User_Pydantic

settings = get_settings()


async def validate_token(reset_token):
    user_token = await UserToken.get(token=reset_token)
    if user_token is not None:
        user_id = copy.deepcopy(user_token.user_id)
        diff = (
            datetime.now() - timezone.make_naive(
                    user_token.created_at, timezone=None
                )
        )
        if diff.total_seconds() < 300:
            await UserToken.filter(token=reset_token).delete()
            return {"status_code": status.HTTP_200_OK, "user": user_id}
        await UserToken.filter(token=reset_token).delete()
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Token Expired")
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid Token")


async def create_verification_token(user):
    user_token_obj = await UserToken(id=uuid.uuid4())
    user_token_obj.created_at = datetime.now()
    user_token_obj.user = user
    await user_token_obj.save()
    return await user_token_obj

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def authenticate_user(username: str, password: str):
    user = await User.get_or_none(email=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user = await User.get(id=payload.get("id"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return await User_Pydantic.from_tortoise_orm(user)
