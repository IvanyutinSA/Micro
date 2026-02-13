from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class BaseError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Internal server error",
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class ValidationError(BaseError):
    def __init__(
        self,
        detail: str = "Validation error",
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers=headers
        )


class ConflictError(BaseError):
    def __init__(
        self,
        detail: str = "Conflict error",
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            headers=headers
        )


class UnauthorizedError(BaseError):
    def __init__(
        self,
        detail: str = "Unauthorized",
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers
        )


class NotFoundError(BaseError):
    def __init__(
        self,
        detail: str = "Not found",
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers
        )
