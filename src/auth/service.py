from fastapi import HTTPException, status, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.db.models import User
from src.db.coludnary import uploadUserProfile
from src.db.redis import getOTPFromRedis
from .schemas import UserCreateModel, VerifyOTPModel, LoginInModel
from .utils import hash_password, verify_password, create_jwt_token


class AuthService:
    async def __getUserByEmail(self, session: AsyncSession, email: str):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def createUser(
        self,
        session: AsyncSession,
        userData: UserCreateModel,
        imageFile: UploadFile,
    ):
        email = userData.email
        userExist = await self.__getUserByEmail(session, email)
        if userExist:
            raise HTTPException(
                detail="User with this email Already exists",
                status_code=status.HTTP_409_CONFLICT,
            )
        profileUrl = await uploadUserProfile(imageFile)
        hashedPwd = hash_password(userData.password)
        newUser = User(**userData.model_dump())
        newUser.profileUrl = profileUrl
        newUser.hashedPassword = hashedPwd
        newUser.username = "@" + userData.fullName.split(" ")[0]
        session.add(newUser)
        await session.commit()
        await session.refresh(newUser)
        return newUser

    async def login(self, loginCred: LoginInModel, session: AsyncSession):
        user = await self.__getUserByEmail(session, loginCred.email)
        if user is None:
            raise HTTPException(
                detail="Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        # user password and db password matched
        if not verify_password(user.hashedPassword, loginCred.password):
            raise HTTPException(
                detail="Please Check you email or password",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        jwt_token = create_jwt_token({"email": user.email, "full_name": str(user.uid)})
        return {
            "message": "login successfully",
            "token": jwt_token,
        }

    async def verify_opt(self, detail: VerifyOTPModel, session: AsyncSession) -> dict:
        user = await self.__getUserByEmail(session, detail.email)
        if user is None:
            raise HTTPException(
                detail="User does't exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        OTP = await getOTPFromRedis(str(user.uid))
        if OTP is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please resend the OPT, Early one is expired",
            )
        if detail.OTP == OTP:
            return {"message": "user verified successfully"}
        else:
            await session.delete(user)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP Don't matched",
            )
