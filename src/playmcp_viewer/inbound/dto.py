from typing import Self

from pydantic import BaseModel, Field, ConfigDict, HttpUrl

from playmcp_viewer.config import Settings
from playmcp_viewer.outbound.dto import (
    PlaymcpDetailResponse,
    PlaymcpFormattedTool,
    PlaymcpFormattedToolParameter,
)

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
    def of(cls, server: PlaymcpDetailResponse) -> Self:
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


class PlayMCPServerToolParameterDetail(BaseModel):
    """Represents details of a parameter for a tool registered in the PlayMCP hub.

    Attributes:
        name: Name of the parameter.
        type: Type of the parameter.
        description: Optional description of the parameter.
        required: Whether the parameter is required.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(description="Parameter name")
    type: str = Field(description="Parameter type")
    description: str | None = Field(description="Parameter description")
    required: bool = Field(description="Required parameter")

    @classmethod
    def of(cls, parameter: PlaymcpFormattedToolParameter) -> Self:
        return cls(
            name=parameter.name,
            type=parameter.type,
            description=parameter.description,
            required=parameter.required,
        )


class PlayMCPServerToolDetail(BaseModel):
    """Represents a tool registered with a MCP server in the PlayMCP hub.

    Attributes:
        name: Name of the tool.
        description: Optional description of the tool.
        parameters: List of parameters for the tool.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(description="Name of the tool")
    description: str | None = Field(description="Description of the tool")
    parameters: list[PlayMCPServerToolParameterDetail] = Field(
        description="List of tool parameters"
    )

    @classmethod
    def of(cls, tool: PlaymcpFormattedTool) -> Self:
        return cls(
            name=tool.name,
            description=tool.description,
            parameters=[
                PlayMCPServerToolParameterDetail.of(param) for param in tool.parameters
            ],
        )


class PlayMCPServerDetail(BaseModel):
    """MCP Server registered in Playmcp hub.

    Attributes:
        id: MCP server id
        url: MCP server link
        name: MCP server name
        description: MCP server description
        developer: MCP server developer's name
        starter_messages: Example starter messages for the MCP server
        tools: Detailed information about tools provided by the MCP server
        thumbnail: MCP server thumbnail image
        monthly_tool_call_count: monthly tool call count
        total_tool_call_count: total tool call count
        supported_mcp_clients: Clients supported by this MCP server
    """

    model_config = ConfigDict(frozen=True)

    id: str = Field(description="MCP server id")
    url: HttpUrl = Field(description="MCP server Link")
    name: str = Field(description="MCP server name")
    description: str = Field(description="MCP server description")
    developer: str = Field(description="MCP server developer's name")
    starter_messages: list[str] = Field(
        description="Example starter messages for the MCP server"
    )
    tools: list[PlayMCPServerToolDetail] = Field(
        description="Detailed information about tools provided by the MCP server"
    )
    thumbnail: HttpUrl = Field(description="MCP server thumbnail image")
    monthly_tool_call_count: int = Field(description="monthly tool call count")
    total_tool_call_count: int = Field(description="total tool call count")
    supported_mcp_clients: str = Field(
        description="Clients supported by this MCP server"
    )

    @classmethod
    def of(cls, server: PlaymcpDetailResponse) -> Self:
        server.applicable_ai_service_scope
        return cls(
            id=server.id,
            url=f"{settings.kakao_playmcp_endpoint}/mcp/{server.id}",
            name=server.name,
            description=server.description,
            developer=server.developer_name,
            starter_messages=server.starter_messages,
            tools=[PlayMCPServerToolDetail.of(tool) for tool in server.formatted_tools],
            thumbnail=server.image.full_url,
            monthly_tool_call_count=server.monthly_tool_call_count,
            total_tool_call_count=server.total_tool_call_count,
            supported_mcp_clients=server.applicable_ai_service_scope,
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
