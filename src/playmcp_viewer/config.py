from typing import Literal

from fastmcp import FastMCP
from dependency_injector import containers, providers
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    kakao_playmcp_endpoint: str
    environment: Literal["local", "dev", "prod"]


class DIContainer(containers.DeclarativeContainer):
    mcp: FastMCP = providers.Singleton(
        FastMCP,
        name="playmcp viewer",
        strict_input_validation=True,
    )
