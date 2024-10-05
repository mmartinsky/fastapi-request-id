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
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
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

# Another sample endpoint to show correlation in different parts of the app
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    current_correlation_id = correlation_id.get()
    logger.info("Fetching item", item_id=item_id, correlation_id=current_correlation_id)
    return {"item_id": item_id, "correlation_id": current_correlation_id}

# Logging setup at startup for demonstration purposes
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application")

# Logging setup at shutdown for demonstration purposes
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down FastAPI application")

# Run with: uvicorn filename:app --reload
# Ensure you have installed the dependencies asgi_correlation_id, fastapi, and structlog
# pip install fastapi asgi-correlation-id uvicorn structlog