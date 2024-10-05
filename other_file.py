import structlog

from nested import nested_fn


# Configure logging (if not already configured elsewhere)
logger = structlog.getLogger("helper_file")

# Example method that gets called within an endpoint, without needing to pass the logger
async def some_helper_function():
    logger.info("This is a log from a helper function")
    # Perform some action

    return await nested_fn()

