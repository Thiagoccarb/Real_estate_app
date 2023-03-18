import re
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from errors.status_error import StatusError


async def handle_validation_error(_: Request, exc: RequestValidationError):
    for error in exc.errors():
        try:
            msg = error["msg"]
            if "regex" in error["type"]:
                msgs = [error["msg"] for error in exc.errors()]
                fields = [field["loc"][1] for field in exc.errors()]
                description = [
                    item.replace("string", f'`{fields[i]}`') for i, item in enumerate(msgs)
                ]
                description = ", ".join(description).replace('\"','').rstrip(", ")
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={
                        "success": False,
                        "error": {
                            "type": "unprocessable_entity",
                            "description": description,
                        },
                    },
                )
            if msg == "field required":
                fields = ",".join(
                    [str("`" + error["loc"][1] + "`") for error in exc.errors()]
                )

                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "error": {
                            "type": "missing_field",
                            "description": f"missing {fields}",
                        },
                    },
                )
        except IndexError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "error": {
                        "type": "missing_field",
                        "description": f"missing body request",
                    },
                },
            )
        except StatusError as e:
            print(e)
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "error": {"type": e.status, "description": e.message},
                },
            )
        except Exception as e:
            print(e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": {
                        "type": "internal error",
                        "description": "Internal server error.",
                    },
                },
            )
