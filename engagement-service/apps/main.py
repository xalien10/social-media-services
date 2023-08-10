import logging

from fastapi import FastAPI
from scheduler.asyncio import Scheduler

from apps.core.databases import init_db
from apps.engagements.schedulers import init_consumer_schedulers
from apps.engagements.views import router as engagement_router

logging.basicConfig(level="INFO")

app = FastAPI()

app.include_router(engagement_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    # Need to register model signals for trigger
    import apps.engagements.signals

    init_db(app)
    await init_consumer_schedulers(Scheduler())
