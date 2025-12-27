import yaml
import logging
from logging.config import dictConfig

from fastmcp import FastMCP

from playmcp_viewer.config import DIContainer, Settings
from playmcp_viewer.inbound.tool import find_mcp_servers


def mcp() -> FastMCP:
    """
    Entrypoint.
    """

    settings = Settings()
    with open("logging.yaml", "r") as fd:
        logging_config = yaml.safe_load(fd)
        dictConfig(logging_config)

    logger = logging.getLogger("playmcp_viewer")
    logger.info(
        f"load {settings.environment}", extra={"environment": settings.environment}
    )

    mcp: FastMCP = DIContainer().mcp()

    # tools
    mcp.tool(find_mcp_servers)

    return mcp
