from fastapi import HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
import httpx
from starlette.requests import Request

from apps.interactions.schemas import UserSchema
from apps.settings import get_settings

settings = get_settings()


async def authenticate_user(request: Request) -> UserSchema:
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                settings.AUTHENTICATION_VERIFICATION_URL, headers={"Authorization": f"Bearer {param}"}
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authetication service unavailable",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            if response.status_code == status.HTTP_200_OK:
                return UserSchema(**response.json())

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credential"
    )


# TODO: Need to create authenticated request for Post service endpoints
async def get_post_detail(request: Request, post_id: str):
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.POST_SERVICE_URL}/api/v1/posts/{post_id}", headers={"Authorization": f"Bearer {param}"}
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Post service unavailable",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            if response.status_code == status.HTTP_200_OK:
                return response.json()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )
