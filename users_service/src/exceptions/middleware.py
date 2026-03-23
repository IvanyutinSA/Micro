from fastapi import Request, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from src.exceptions.http import BaseError


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except BaseError as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
                headers=exc.headers
            )
        except PydanticValidationError as exc:
            # Handle Pydantic validation errors
            return JSONResponse(
                status_code=422,
                content={"detail": exc.errors()}
            )
        except NoResultFound:
            # Handle SQLAlchemy not found errors
            return JSONResponse(
                status_code=404,
                content={"detail": "Resource not found"}
            )
        except IntegrityError:
            # Handle database integrity errors
            return JSONResponse(
                status_code=400,
                content={"detail":
                         "Database integrity error. Possible duplicate entry."}
            )
        except Exception:
            # Handle all other unexpected errors
            # In production, you might want to log these errors
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
