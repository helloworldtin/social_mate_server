from fastapi import (
    APIRouter,
    status,
    UploadFile,
    BackgroundTasks,
    Depends,
    File,
    Form,
    Body,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Annotated

from src.db.main import get_session
from src.db.redis import getOTPFromRedis, putOPTInRedis
from src.mail import createMessage, mail, otpHtmlMessage
from .service import AuthService
from .utils import createOTP
from .schemas import UserCreateModel, UserModel, VerifyOTPModel, LoginInModel

authRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

authService = AuthService()


@authRouter.post(
    "/create_user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    fullName: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    bio: Annotated[str, Form()],
    imageFile: Annotated[UploadFile, File()],
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    userData = UserCreateModel(
        fullName=fullName, email=email, password=password, bio=bio
    )
    user = await authService.createUser(session, userData, imageFile)
    OTP = createOTP()
    await putOPTInRedis(OTP, str(user.uid))
    message = createMessage(
        recipients=[user.email], body=otpHtmlMessage(OTP), subject="Your OTP"
    )
    background_task.add_task(mail.send_message, message=message)
    return user


@authRouter.post("/login")
async def login_user(
    loginCred: LoginInModel, session: AsyncSession = Depends(get_session)
):
    return await authService.login(loginCred, session)


@authRouter.post("/verify-opt")
async def verify_opt(
    verification_details: Annotated[VerifyOTPModel, Body()],
    session: AsyncSession = Depends(get_session),
):
    return await authService.verify_opt(verification_details, session)
