import yaml
import logging
from logging.config import dictConfig

from fastmcp import FastMCP
from playmcp_viewer.config import Settings

settings = Settings()
with open("logging.yaml", "r") as fd:
    logging_config = yaml.safe_load(fd)
    dictConfig(logging_config)

logger = logging.getLogger("playmcp_viewer")
logger.info(f"load {settings.environment}", extra={"environment": settings.environment})

mcp = FastMCP(
    name="playmcp viewer",
)

@mcp.tool
async def hello(message: str) -> str:
    """
    say hi.
    """
    return "hi"