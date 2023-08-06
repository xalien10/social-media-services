import logging

from fastapi import FastAPI
from scheduler.asyncio import Scheduler

from apps.core.databases import init_db
from apps.posts.schedulers import init_consumer_schedulers
from apps.posts.views import router as post_router

logging.basicConfig(level="INFO")

app = FastAPI()

app.include_router(post_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    # Need to register model signals for trigger
    import apps.posts.signals

    init_db(app)
    await init_consumer_schedulers(Scheduler())
