from pydantic import BaseModel, Field, ConfigDict, HttpUrl


class PlayMCPServer(BaseModel):
    """MCP Server registered in Playmcp hub.

    Attributes:
        url: MCP server link
        name: MCP server name
        description: MCP server description
        developer: MCP server developer's name
        thumbnail: MCP server thumbnail image
        monthly_tool_call_count: monthly tool call count
        total_tool_call_count: total tool call count
    """

    model_config = ConfigDict(frozen=True)

    url: HttpUrl = Field(description="MCP server Link")
    name: str = Field(description="MCP server name")
    description: str = Field(description="MCP server description")
    developer: str = Field(description="MCP server developer's name")
    thumbnail: HttpUrl = Field(description="MCP server thumbnail image")
    monthly_tool_call_count: int = Field(description="monthly tool call count")
    total_tool_call_count: int = Field(description="total tool call count")
