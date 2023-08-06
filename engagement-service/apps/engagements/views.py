from fastapi import Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from tortoise.exceptions import DoesNotExist

from apps.engagements.schemas import (
    UserEngagement,
    UserEngagement_Pydantic,
    UserSchema,
)
from apps.core.security import (
    authenticate_user,
)

router = InferringRouter(tags=["activity-profile"])


@cbv(router)
class EngagementViews:

    current_user: UserSchema = Depends(authenticate_user)

    @router.get("/me/activity-profile", response_model=UserEngagement_Pydantic, status_code=status.HTTP_200_OK)
    async def retrieve_activity_profile(self):
        try:
            profile = await UserEngagement.get(user_id=self.current_user.id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User engagement profile not found"
            )
        return await UserEngagement_Pydantic.from_tortoise_orm(profile)
