from fastapi import APIRouter, Depends, Body, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Annotated

from src.db.main import get_session
from src.errors import UserNotFound

from .service import AuthService
from .utils import create_jwt_token
from .schemas import UserModel, UserCreateModel, UserUpdateModel

auth_router = APIRouter()
session: AsyncSession = Depends(get_session)
user_service = AuthService()


@auth_router.post("/register", response_model=UserModel)
async def create_user(user_data: Annotated[UserCreateModel, Body()], session=session):
    return await user_service.create_user(user_data, session)


@auth_router.get('/login/{email}')
async def login_user(email:Annotated[str,Path()],session = session):
    user_exist = await user_service.user_exist(email,session) 
    if not user_exist:
        raise UserNotFound()
    token =  create_jwt_token({'email':email}) 
    return {
        "message" : "login successfully",
        "token" : token
    }
    

@auth_router.get("/users/{username}",response_model=UserModel)
async def searchUser(username: str, session=session):
    return await user_service.search_user_by_username(username, session)


@auth_router.post("/update_user/{user_email}", response_model=UserModel)
async def update_user(
    user_email: Annotated[str, Path()],
    update_data: Annotated[UserUpdateModel, Body()],
    session=session,
):

    updated_user = await user_service.update_user_expect_pass(
        user_email, update_data, session
    )
    return updated_user
