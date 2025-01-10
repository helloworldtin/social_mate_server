from typing import Coroutine, Any
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from .utils import decode_jwt_token


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Coroutine[Any, Any, HTTPAuthorizationCredentials | None]:
        credentials = await super().__call__(request)
        token = credentials.credentials
        token_data = decode_jwt_token(token=token)
        if token_data is None:
            raise HTTPException(status_code=400, detail="You token is invalid")

        return token_data
