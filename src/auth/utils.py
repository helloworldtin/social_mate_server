from argon2 import PasswordHasher
from jwt.exceptions import PyJWTError
import jwt

import random
from uuid import uuid4

from src.config import Config


ph = PasswordHasher()


def hash_password(password: str) -> str:
    hashed_password = ph.hash(password)
    return hashed_password


def verify_password(hashed_password: str, actual_password: str) -> bool:
    try:
        return ph.verify(hashed_password, actual_password)
    except:
        return False


def create_jwt_token(user_data: dict) -> str:
    payload = {}
    payload["user"] = user_data
    payload["jti"] = str(uuid4())

    token = jwt.encode(
        payload=payload, algorithm=Config.JWT_ALGO, key=Config.JWT_SECRETE
    )
    return token


def decode_jwt_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRETE, algorithms=[Config.JWT_ALGO]
        )
        return token_data
    except PyJWTError as e:
        print(e)
        return None
    except:
        print("error in decoding jwt")
        return None


def createOTP() -> str:
    opt = ""
    for _ in range(6):
        opt += str(random.randint(0, 9))
    return opt
