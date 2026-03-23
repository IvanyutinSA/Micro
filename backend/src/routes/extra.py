from src.exceptions.http import UnauthorizedError
from src.utilities.jwt import decode_token, verify_token as vt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]
                        ) -> int:
    if not vt(token):
        raise UnauthorizedError("Token expired")
    payload = decode_token(token)
    return payload["user_id"]
