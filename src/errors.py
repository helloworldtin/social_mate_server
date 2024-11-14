from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse

from typing import Callable, Any


class PostExceptions(Exception):
    """this is the core exception"""

    pass


class UserNotFound(PostExceptions):
    pass


class UserAlreadyExist(PostExceptions):
    pass


class InvalidToken(PostExceptions):
    pass


def crete_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Response, Exception], JSONResponse]:
    async def exception_handler(request: Request, exec: PostExceptions):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI) -> None:
    @app.exception_handler(500)
    async def internal_server_error(request: Request, exception: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Oops Something went wrong",
                "error_code": "server_error",
            },
        )

    app.add_exception_handler(
        UserNotFound,
        crete_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "user not found"},
        ),
    )
    app.add_exception_handler(
        UserAlreadyExist,
        crete_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={"message": "user with this email already exist"},
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        crete_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Invalid token"},
        ),
    )
