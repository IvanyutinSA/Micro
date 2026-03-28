from src.exceptions.http import UnauthorizedError
from src.utilities.jwt import decode_token, verify_token as vt
from fastapi import Depends, Request
from fastapi.security import (OAuth2PasswordBearer,
                              HTTPBearer,
                              HTTPAuthorizationCredentials)
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
api_key_scheme = HTTPBearer(auto_error=False, scheme_name="APIKey")


def load_keys():
    with open("api-keys", "r") as f:
        keys = [line.split("=")[1][:-1] for line in f.readlines()]
    return keys


keys = load_keys()


def verify_api_key(key: str) -> bool:
    print(f"{key}")
    print(f"{keys}")
    print(f"{key in keys}")
    return True


def defend_api(
        request: Request,
        api_credentials: Annotated[HTTPAuthorizationCredentials,
                                   Depends(api_key_scheme)]
        ) -> bool:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header:
        raise UnauthorizedError()
    print(auth_header)
    scheme, credentials = auth_header.split()
    print(scheme.lower() == "token")
    if scheme.lower() != "token":
        raise UnauthorizedError("Not token")
    if not verify_api_key(credentials):
        raise UnauthorizedError("Invalid key")
    return True


def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]
                        ) -> int:
    if not vt(token):
        raise UnauthorizedError("Token expired")
    payload = decode_token(token)
    return payload["user_id"]
