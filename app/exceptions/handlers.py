from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import SmartJobException
from app.utils.logger import logger


async def smartjob_exception_handler(
    request: Request,
    exc: SmartJobException
):

    logger.error(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": exc.message
        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(str(exc))

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "An unexpected error occurred."
        }
    )