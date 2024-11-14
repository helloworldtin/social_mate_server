from typing import Coroutine, Any
from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from src.errors import InvalidToken
from .utils import decode_token


class TokenBearerVerify(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Coroutine[Any, Any, HTTPAuthorizationCredentials | None]:
        credentials = await super().__call__(request)
        token = credentials.credentials
        token_data = decode_token(token=token)
        if token_data is None:
            raise InvalidToken()
        
        return token_data
