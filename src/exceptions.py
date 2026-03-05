from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class CustomException(Exception):
    """
    Params:
        msg* (string): Message for output
        code (string): Additional id exception for some purposes
    """

    def __init__(self, msg: str, code: str = None) -> None:
        super().__init__()
        self.msg = msg
        self.code = code

    def __str__(self) -> str:
        return self.msg

    def to_json(self) -> dict:
        return {
            "message": self.msg,
            "code": self.code,
        }


class ClientError(CustomException): ...


class ObjectNotFound(CustomException): ...


class AccessForbidden(CustomException): ...


class CustomValidationError(CustomException): ...


class NetworkError(CustomException): ...


async def uncaught_exception(request: Request, exc: Exception) -> JSONResponse:
    exc = CustomException(msg="Unknown error, please, try again later")
    return JSONResponse(content=exc.to_json(), status_code=500)


async def no_result_found(request: Request, exc: ObjectNotFound) -> JSONResponse:
    return JSONResponse(content=exc.to_json(), status_code=404)


async def access_forbidden(request: Request, exc: ObjectNotFound) -> JSONResponse:
    return JSONResponse(content=exc.to_json(), status_code=403)


async def client_error(request: Request, exc: ClientError) -> JSONResponse:
    return JSONResponse(content=exc.to_json(), status_code=400)


async def validation_error(request: Request, exc: CustomValidationError) -> JSONResponse:
    return JSONResponse(content=exc.to_json(), status_code=400)


async def no_network(request: Request, exc: NetworkError) -> JSONResponse:
    return JSONResponse(content=exc.to_json(), status_code=502)


def connect_all_exceptions_to_handler(app: FastAPI) -> None:
    app.add_exception_handler(Exception, uncaught_exception)
    app.add_exception_handler(ObjectNotFound, no_result_found)
    app.add_exception_handler(AccessForbidden, access_forbidden)
    app.add_exception_handler(ClientError, client_error)
    app.add_exception_handler(CustomValidationError, validation_error)
    app.add_exception_handler(NetworkError, no_network)
