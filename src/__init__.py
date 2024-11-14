from fastapi import FastAPI
from .errors import register_all_errors

from src.auth.routes import auth_router
from src.post.routes import post_router

app = FastAPI()

app.include_router(auth_router,prefix='/auth',tags=['authentication'])
app.include_router(post_router,prefix='/post',tags=['post'])

register_all_errors(app)