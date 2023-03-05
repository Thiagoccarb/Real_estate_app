from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from error_handlers.status_error_handler import handle_status_error_exception
from errors.status_error import StatusError
from error_handlers.validation_error_handler import handle_validation_error

from database.migrations.update import upgrade_database
from config.settings import settings
from database.create import create_database
from routes import app_router


app = FastAPI(
    routes=app_router.routes,
    title=settings.NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
)


@app.on_event("startup")
async def startup():
    await create_database()
    await upgrade_database()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await handle_validation_error(request, exc)


@app.exception_handler(StatusError)
async def handle_exception(_, exc: StatusError):
    return await handle_status_error_exception(exc)


app.add_middleware(GZipMiddleware, minimum_size=1000)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        print(e)
        error_msg = {
            "success": False,
            "error": {
                "type": "internal_server_error",
                "description": "--! Internal Server Error",
            },
        }
        return JSONResponse(content=error_msg, status_code=500)
    return response
