import asyncio
from typing import Literal
from collections import defaultdict

from fastmcp import FastMCP
from fastmcp.server.context import Context
from fastmcp.dependencies import CurrentContext

from playmcp_viewer.config import DIContainer, Settings
from playmcp_viewer.outbound.client import get_playmcp_list
from playmcp_viewer.inbound.dto import DeveloperInfo, PlayMCPServer
from playmcp_viewer.outbound.dto import PlaymcpListContentResponse, PlaymcpListResponse

settings = Settings()
mcp: FastMCP = DIContainer().mcp()


async def find_mcp_servers(
    cond: Literal["TOTAL_TOOL_CALL_COUNT", "FEATURED_LEVEL", "CREATED_AT"],
    top_n: int | None = None,
    developer: str | None = None,
    order_by: Literal["asc", "desc"] = "desc",
    ctx: Context = CurrentContext(),
) -> list[PlayMCPServer]:
    """
    Retrieve a list of MCP servers registered on the Kakao PlayMCP platform, sorted by the specified condition and order.

    Tool Parameters:
        cond: The field to sort by. One of "TOTAL_TOOL_CALL_COUNT", "FEATURED_LEVEL", or "CREATED_AT".
        order_by: Sorting direction. Must be "asc" for ascending or "desc" for descending.
        top_n: Number of top MCP servers to return. If not specified, all servers will be returned.
        developer: Developer name to filter by. If not provided, all MCP servers will be returned.
    Returns:
        A list of PlayMCPServer objects, each containing:
            url: URL of the MCP server.
            name: Name of the MCP server.
            description: Description of the MCP server.
            developer: Developer name of the MCP server.
            thumbnail: Thumbnail image URL of the MCP server.
            monthly_tool_call_count: Monthly tool call count.
            total_tool_call_count: Total tool call count.
    """

    page: int = 0
    playmcp_contents: list[PlaymcpListContentResponse] = []
    while True:
        playmcp_resp: PlaymcpListResponse = await get_playmcp_list(
            trace_id=ctx.request_id,
            page=page,
            sort_by=cond,
        )

        playmcp_contents.extend(playmcp_resp.content)

        if page + 1 == playmcp_resp.total_pages:
            break
        page += 1

        await asyncio.sleep(0.1)

    if order_by == "asc":
        playmcp_contents = playmcp_contents[::-1]
    if developer:
        playmcp_contents = [
            content
            for content in playmcp_contents
            if content.developer_name == developer
        ]

    playmcp_contents = playmcp_contents[:top_n]

    resp = [
        PlayMCPServer(
            url=f"{settings.kakao_playmcp_endpoint}/mcp/{content.id}",
            name=content.name,
            description=content.description,
            developer=content.developer_name,
            thumbnail=content.image.full_url,
            monthly_tool_call_count=content.monthly_tool_call_count,
            total_tool_call_count=content.total_tool_call_count,
        )
        for content in playmcp_contents
    ]
    return resp


async def group_by_developer(
    developer: str | None = None,
    min_mcp_server_count: int | None = None,
    order_by: Literal["asc", "desc"] = "desc",
    ctx: Context = CurrentContext(),
) -> list[DeveloperInfo]:
    """
    Find developers and their MCP servers registered in Playmcp hub.

    Tool Parameters:
        developer: Developer name to filter by. If not provided, all developers will be returned.
        min_mcp_server_count: Only include developers who have at least this many registered MCP servers. If not specified, all developers are included.
        order_by: Determines the sort order of developers by the number of MCP servers they have registered. Accepts "asc" for ascending order or "desc" for descending order.
    Returns:
        A list of DeveloperInfo objects, each containing:
            name: Developer name
            mcp_servers: MCP servers registered by the developer
    """
    mcp_servers: list[PlayMCPServer] = await find_mcp_servers(
        cond="TOTAL_TOOL_CALL_COUNT",
        order_by="desc",
        developer=developer,
        ctx=ctx,
    )
    developer_infos: dict[str, list[PlayMCPServer]] = defaultdict(list)
    for mcp_server in mcp_servers:
        developer_infos[mcp_server.developer].append(mcp_server)
    resp = [
        DeveloperInfo(
            name=developer,
            mcp_servers=mcp_servers,
        )
        for developer, mcp_servers in developer_infos.items()
    ]

    if min_mcp_server_count:
        resp = [x for x in resp if len(x.mcp_servers) >= min_mcp_server_count]
    
    resp = sorted(resp, key=lambda x: len(x.mcp_servers), reverse="desc" == order_by)
    return resp