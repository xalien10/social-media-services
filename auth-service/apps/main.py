from fastapi import FastAPI

from apps.core.databases import init_db
from apps.users.views import router as user_router


app = FastAPI()

app.include_router(user_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    # startup needs model signal registration
    import apps.users.signals

    init_db(app)
