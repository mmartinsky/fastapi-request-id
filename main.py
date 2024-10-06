# Import necessary modules
from asyncio import sleep
from typing import Any
from fastapi import FastAPI, Request
from asgi_correlation_id import CorrelationIdMiddleware, correlation_id
import structlog
import sys
import logging

from other_file import some_helper_function

def add_correlation(
    logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add request id to log message."""
    if request_id := correlation_id.get():
        event_dict["request_id"] = request_id
    return event_dict

# Configure structlog to print to console
structlog.configure(
    processors=[
        add_correlation,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer()  # Use ConsoleRenderer to print to console
    ],
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize the FastAPI app
app = FastAPI()

# Add CorrelationIdMiddleware to the FastAPI app
app.add_middleware(CorrelationIdMiddleware)

# Sample endpoint to demonstrate correlation ID
@app.get("/")
async def read_root(request: Request):
    # Get the correlation ID from the request context
    current_correlation_id = correlation_id.get()
    
    # Log a message that includes the correlation ID
    logger.info("Handling request")
    await sleep(2)

    await some_helper_function()
    await sleep(2)

    logger.info("Finished request")
    return {"message": "Hello, world!", "correlation_id": current_correlation_id}

# Run with: uvicorn filename:app --reload
# Ensure you have installed the dependencies asgi_correlation_id, fastapi, and structlog
# pip install fastapi asgi-correlation-id uvicorn structlog