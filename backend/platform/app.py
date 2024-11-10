from fastapi import FastAPI

from router.dev import router as dev_router
from db.init_db import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(dev_router, prefix="/dev")
