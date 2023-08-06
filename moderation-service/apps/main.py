import logging

from fastapi import FastAPI
from scheduler.asyncio import Scheduler

from apps.core.databases import init_db
from apps.moderations.schedulers import init_consumer_schedulers

logging.basicConfig(level="INFO")

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Need to register signals
    import apps.moderations.signals

    init_db(app)
    await init_consumer_schedulers(Scheduler())
