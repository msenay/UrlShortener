import logging
import os

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import url_shortener

from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response

REQUEST_COUNT = Counter("request_count", "Total HTTP requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency", ["method", "endpoint"])


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        method = request.method
        endpoint = request.url.path
        with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
            response = await call_next(request)
            status_code = response.status_code
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
            return response


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
API_PORT = int(os.getenv("API_PORT", 8001))

app = FastAPI()

# Add the middleware to your FastAPI application
app.add_middleware(MetricsMiddleware)

# Include routers
app.include_router(url_shortener.router, tags=["url_shortener"])


# Exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Exception handler for validation errors.

    Args:
        request: request.
        exc: raised error.

    Returns:
        JSONResponse: details about the validation error.
    """
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 422, "message": exc_str, "data": None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


# Health check endpoint
@app.get("/ping")
async def ping():
    """
    Ping endpoint to check the service status.
    This endpoint is used to verify if the service is running.
    It returns a simple "pong" message.
    Returns:
        str: A "pong" message.
    """
    return "pong"


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)
