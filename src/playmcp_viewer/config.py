from typing import Literal
from logging.config import dictConfig

import yaml
import structlog
from fastmcp import FastMCP
from dependency_injector import containers, providers
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    kakao_playmcp_endpoint: str
    tool_call_limit_per_second: int
    environment: Literal["local", "dev", "prod"]


class DIContainer(containers.DeclarativeContainer):
    mcp: FastMCP = providers.Singleton(
        FastMCP,
        name="playmcp viewer",
        strict_input_validation=True,
    )


class JSONFormatter(structlog.stdlib.ProcessorFormatter):
    """
    JSON formatter for structlog with proper Unicode support for Korean characters.
    """

    def __init__(self, **kwargs):
        # Remove any conflicting keys that might be passed from dictConfig
        kwargs.pop("processor", None)
        kwargs.pop("foreign_pre_chain", None)

        # Configure the processor with Unicode support
        processor = structlog.processors.JSONRenderer(
            ensure_ascii=False,  # Preserve Korean characters
            indent=4,
        )

        # Configure foreign_pre_chain for non-structlog loggers
        foreign_pre_chain = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.ExtraAdder(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
        ]

        super().__init__(
            processor=processor,
            foreign_pre_chain=foreign_pre_chain,
            **kwargs,
        )


def configure_log(config):
    # Configure structlog early so formatters can use it
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging_config = yaml.safe_load(config)
    dictConfig(logging_config)
