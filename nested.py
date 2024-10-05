import structlog

# Configure logging (if not already configured elsewhere)
logger = structlog.getLogger("nested")

# Example method that gets called within an endpoint, without needing to pass the logger
async def nested_fn():
    logger.info("This is a nested log")
    # Perform some action
    return "Helper function result"

