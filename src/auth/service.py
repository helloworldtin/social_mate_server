from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.errors import UserNotFound,UserAlreadyExist
from .utils import hash_password
from .schemas import UserCreateModel, UserUpdateModel


class AuthService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exist(self, email: str, session: AsyncSession) -> bool:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first() is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        if await self.user_exist(user_data.email, session):
            raise UserAlreadyExist()
        user_data.password = hash_password(user_data.password)
        user = User(**user_data.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def search_user_by_username(self,username: str, session: AsyncSession) -> User:
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        if user is None:
            raise UserNotFound()
        return user

    async def update_user_expect_pass(
        self, user_email: str, update_data: UserUpdateModel, session: AsyncSession
    ):
        """
        <h1>change the data of the user excluding password</h1>
        """

        user = await self.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()
        for k, v in update_data.model_dump().items():
            if v is None:
                continue
            setattr(user, k, v)
        await session.commit()
        await session.refresh(user)
        return user
