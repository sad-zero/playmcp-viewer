import asyncio
from typing import Literal
from collections import defaultdict

from fastmcp import FastMCP
from fastmcp.server.context import Context
from fastmcp.exceptions import ValidationError
from fastmcp.dependencies import CurrentContext

from playmcp_viewer.inbound.dto import (
    DeveloperInfo,
    PlayMCPServer,
    PlayMCPServerBriefInfo,
)
from playmcp_viewer.config import DIContainer, Settings
from playmcp_viewer.outbound.client import get_playmcp_list
from playmcp_viewer.outbound.dto import PlaymcpListContentResponse, PlaymcpListResponse

settings = Settings()
mcp: FastMCP = DIContainer().mcp()


async def find_mcp_servers(
    cond: Literal["TOTAL_TOOL_CALL_COUNT", "FEATURED_LEVEL", "CREATED_AT"],
    top_n: int,
    developer: str | None = None,
    order_by: Literal["asc", "desc"] = "desc",
    ctx: Context = CurrentContext(),
) -> list[PlayMCPServer]:
    """
    Retrieve a list of MCP servers registered on the Kakao PlayMCP platform, sorted by the specified condition and order.

    Tool Parameters:
        cond: The field to sort by. One of "TOTAL_TOOL_CALL_COUNT", "FEATURED_LEVEL", or "CREATED_AT".
        order_by: Sorting direction. Must be "asc" for ascending or "desc" for descending.
        top_n: The maximum number of MCP servers to return (up to 50). If not specified, all servers will be returned.
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
    if top_n > 50:
        raise ValidationError(f"top_n({top_n}) > 50")

    playmcp_contents = await _find_mcp_servers(
        cond,
        ctx,
    )

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
        PlayMCPServer.of(content)
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
    playmcp_contents: list[PlaymcpListContentResponse] = await _find_mcp_servers(
        cond="TOTAL_TOOL_CALL_COUNT",
        ctx=ctx,
    )
    mcp_servers = [
        PlayMCPServer.of(content)
        for content
        in playmcp_contents
    ]
    developer_infos: dict[str, list[PlayMCPServerBriefInfo]] = defaultdict(list)
    for mcp_server in mcp_servers:
        brief_info = PlayMCPServerBriefInfo.of(mcp_server)
        developer_infos[mcp_server.developer].append(brief_info)
    resp = [
        DeveloperInfo(
            name=developer,
            mcp_servers=mcp_servers,
        )
        for developer, mcp_servers in developer_infos.items()
    ]

    if developer:
        resp = [x for x in resp if x.name == developer]

    if min_mcp_server_count:
        resp = [x for x in resp if len(x.mcp_servers) >= min_mcp_server_count]

    resp = sorted(resp, key=lambda x: len(x.mcp_servers), reverse="desc" == order_by)
    return resp


async def _find_mcp_servers(
    cond: str,
    ctx: Context = CurrentContext(),
) -> list[PlaymcpListContentResponse]:
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
    return playmcp_contents
