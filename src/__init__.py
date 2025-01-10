from fastapi import FastAPI

from src.auth.routes import authRouter

app = FastAPI()

app.include_router(authRouter)
