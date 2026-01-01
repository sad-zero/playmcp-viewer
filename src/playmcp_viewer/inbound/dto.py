from typing import Self

from pydantic import BaseModel, Field, ConfigDict, HttpUrl

from playmcp_viewer.config import Settings
from playmcp_viewer.outbound.dto import PlaymcpListContentResponse

settings = Settings()


class PlayMCPServer(BaseModel):
    """MCP Server registered in Playmcp hub.

    Attributes:
        id: MCP server id
        url: MCP server link
        name: MCP server name
        description: MCP server description
        developer: MCP server developer's name
        thumbnail: MCP server thumbnail image
        monthly_tool_call_count: monthly tool call count
        total_tool_call_count: total tool call count
    """

    model_config = ConfigDict(frozen=True)

    id: str = Field(description="MCP server id")
    url: HttpUrl = Field(description="MCP server Link")
    name: str = Field(description="MCP server name")
    description: str = Field(description="MCP server description")
    developer: str = Field(description="MCP server developer's name")
    thumbnail: HttpUrl = Field(description="MCP server thumbnail image")
    monthly_tool_call_count: int = Field(description="monthly tool call count")
    total_tool_call_count: int = Field(description="total tool call count")

    @classmethod
    def of(cls, server: PlaymcpListContentResponse) -> Self:
        return cls(
            id=server.id,
            url=f"{settings.kakao_playmcp_endpoint}/mcp/{server.id}",
            name=server.name,
            description=server.description,
            developer=server.developer_name,
            thumbnail=server.image.full_url,
            monthly_tool_call_count=server.monthly_tool_call_count,
            total_tool_call_count=server.total_tool_call_count,
        )


class PlayMCPServerBriefInfo(BaseModel):
    """MCP Server registered in Playmcp hub.

    Attributes:
        id: MCP server id
        url: MCP server link
        name: MCP server name
    """

    model_config = ConfigDict(frozen=True)

    id: str = Field(description="MCP server id")
    url: HttpUrl = Field(description="MCP server Link")
    name: str = Field(description="MCP server name")

    @classmethod
    def of(cls, mcp_server: PlayMCPServer) -> Self:
        return cls(
            id=mcp_server.id,
            url=mcp_server.url,
            name=mcp_server.name,
        )


class DeveloperInfo(BaseModel):
    """Developer information grouped by developer name.

    Attributes:
        name: Developer name
        mcp_servers: MCP servers registered by the developer
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(description="Developer name")
    mcp_servers: list[PlayMCPServerBriefInfo] = Field(
        description="Developer's MCP servers"
    )
