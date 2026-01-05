import asyncio
from typing import Literal
from collections import defaultdict

from fastmcp.server.context import Context
from fastmcp.dependencies import CurrentContext
from fastmcp.exceptions import ValidationError, NotFoundError
from mcp.types import Content

from playmcp_viewer.inbound.dto import (
    DeveloperInfo,
    PlayMCPServer,
    PlayMCPServerDetail,
    PlayMCPServerBriefInfo,
)
from playmcp_viewer.outbound.client import get_playmcp_list, get_playmcp_server
from playmcp_viewer.outbound.dto import PlaymcpDetailResponse, PlaymcpListResponse


async def find_mcp_servers(
    cond: Literal["TOTAL_TOOL_CALL_COUNT", "FEATURED_LEVEL", "CREATED_AT"],
    top_n: int,
    developer: str | None = None,
    min_monthly_tool_call_count: int | None = None,
    min_total_tool_call_count: int | None = None,
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
        min_monthly_tool_call_count: Minimum monthly tool call count to filter MCP servers. If not provided, no filtering is applied.
        min_total_tool_call_count: Minimum total tool call count to filter MCP servers. If not provided, no filtering is applied.

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

    if developer:
        playmcp_contents = [
            content
            for content in playmcp_contents
            if content.developer_name == developer
        ]
    if min_monthly_tool_call_count:
        playmcp_contents = [
            content
            for content in playmcp_contents
            if content.monthly_tool_call_count >= min_monthly_tool_call_count
        ]
    if min_total_tool_call_count:
        playmcp_contents = [
            content
            for content in playmcp_contents
            if content.total_tool_call_count >= min_total_tool_call_count
        ]
    if order_by == "asc":
        playmcp_contents = playmcp_contents[::-1]

    playmcp_contents = playmcp_contents[:top_n]

    resp = [PlayMCPServer.of(content) for content in playmcp_contents]
    return resp


async def group_by_developer(
    developer: str | None = None,
    min_mcp_server_count: int | None = None,
    is_active: bool | None = None,
    order_by: Literal["asc", "desc"] = "desc",
    ctx: Context = CurrentContext(),
) -> list[DeveloperInfo]:
    """
    Find developers and their MCP servers registered in Playmcp hub.

    Tool Parameters:
        developer: (optional) Filter by developer name. If not provided, include all developers.
        min_mcp_server_count: (optional) Minimum number of MCP servers a developer must have registered to be included. Defaults to including all.
        is_active: (optional) If True, only include developers where at least one of their MCP servers has a monthly tool call count greater than 10. If False, include only those where none of their MCP servers exceeds 10. If not provided, include all developers.
        order_by: (optional) Sort order for developers by their registered MCP server count. "asc" for ascending, "desc" for descending (default: "desc").
    Returns:
        A list of DeveloperInfo objects, each containing:
            name: Developer name
            mcp_servers: MCP servers registered by the developer
    """
    playmcp_contents: list[PlaymcpDetailResponse] = await _find_mcp_servers(
        cond="TOTAL_TOOL_CALL_COUNT",
        ctx=ctx,
    )
    mcp_servers = [PlayMCPServer.of(content) for content in playmcp_contents]
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

    if is_active is False:
        resp = [
            x for x in resp if not any(server.is_active for server in x.mcp_servers)
        ]

    if is_active is True:
        resp = [x for x in resp if any(server.is_active for server in x.mcp_servers)]

    resp = sorted(resp, key=lambda x: len(x.mcp_servers), reverse="desc" == order_by)
    return resp


async def find_mcp_server_by_id(
    id: str,
    ctx: Context = CurrentContext(),
) -> PlayMCPServerDetail:
    """
    Retrieve detailed information about a specific MCP server registered in the PlayMCP hub.

    Tool Parameters:
        id: MCP server id

    Returns:
        A PlayMCPServerDetail object with the following information:
            id: MCP server id
            url: MCP server link
            name: MCP server name
            description: MCP server description
            developer: MCP server developer's name
            starter_messages: Example starter messages for the MCP server
            tools: Detailed information about tools provided by the MCP server
            thumbnail: MCP server thumbnail image
            monthly_tool_call_count: Monthly tool call count
            total_tool_call_count: Total tool call count
            supported_mcp_clients: Clients supported by this MCP server
    """
    playmcp = await get_playmcp_server(
        trace_id=ctx.request_id,
        server_id=id,
    )
    if playmcp:
        return PlayMCPServerDetail.of(playmcp)
    raise NotFoundError(f"mcp server {id} not found")


async def _find_mcp_servers(
    cond: str,
    ctx: Context = CurrentContext(),
) -> list[PlaymcpDetailResponse]:
    page: int = 0
    playmcp_contents: list[PlaymcpDetailResponse] = []
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
