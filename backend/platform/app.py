from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.dev import router as dev_router

app: FastAPI = FastAPI()

# Should be coming from config/env
origins: list[str] = [
    "http://localhost:5812",
    "http://127.0.0.1:5812",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dev_router, prefix="/dev")
