from src.utilities.jwt import decode_token, verify_token as vt
from src.schemas import GetUserRequest
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def verify_token(token: Annotated[str, Depends(oauth2_scheme)]
                 ) -> GetUserRequest:
    return verify_token()


def get_current_user_req(token: Annotated[str, Depends(oauth2_scheme)]
                         ) -> GetUserRequest:
    vt(token)
    payload = decode_token(token)
    request = GetUserRequest(username=payload.get("sub", ""))
    return request
