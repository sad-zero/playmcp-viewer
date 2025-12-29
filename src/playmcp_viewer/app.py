import logging

from fastmcp import FastMCP
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.caching import ResponseCachingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

from playmcp_viewer.config import DIContainer, Settings, configure_log
from playmcp_viewer.inbound.tool import find_mcp_servers


def mcp() -> FastMCP:
    """
    Entrypoint.
    """

    settings = Settings()
    with open("logging.yaml", "r") as fd:
        configure_log(fd)

    logger = logging.getLogger("playmcp_viewer")
    logger.info(
        f"load {settings.environment}", extra={"environment": settings.environment}
    )

    mcp: FastMCP = DIContainer().mcp()

    # tools
    mcp.tool(find_mcp_servers)

    # middlewares.
    mcp.add_middleware(
        ErrorHandlingMiddleware(
            include_traceback=True,
            logger=logging.getLogger("playmcp_viewer.middlewre.error_handler"),
        )
    )
    mcp.add_middleware(
        TimingMiddleware(
            logger=logging.getLogger("playmcp_viewer.middleware.timing"),
        )
    )
    # TODO: log response even if caching.
    mcp.add_middleware(
        LoggingMiddleware(
            logger=logging.getLogger("playmcp_viewer.middleware.logging"),
            include_payloads=True,
        )
    )
    mcp.add_middleware(ResponseCachingMiddleware())
    mcp.add_middleware(
        RateLimitingMiddleware(
            max_requests_per_second=settings.tool_call_limit_per_second,
            global_limit=True,
        )
    )

    return mcp
