from dotenv import load_dotenv
from jose import jwt
from time import time
import os

load_dotenv()
HASH_SECRET = os.environ.get("HASH_SECRET", "secret")
ACCESS_TOKEN_DELTA_MINUTES = int(os.environ.get("ACCESS_TOKEN_DELTA_MINUTES",
                                                30))
ALGORITHM = os.environ.get("ALGORITH", "HS256")


def create_access_token(sub: str, extra: dict = {}) -> str:
    token = extra.copy()
    token["sub"] = extra.get("sub", sub)
    token["exp"] = time()+ACCESS_TOKEN_DELTA_MINUTES*60
    token = jwt.encode(token, HASH_SECRET, ALGORITHM)
    return token


def decode_token(token: str) -> str:
    return jwt.decode(token, HASH_SECRET, ALGORITHM)


def verify_token(token: str) -> bool:
    payload = decode_token(token)
    if payload.get("exp", 0) < time():
        return False
    return True
