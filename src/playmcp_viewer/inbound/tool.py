from typing import Literal
from fastmcp import FastMCP
from fastmcp.server.context import Context
from fastmcp.dependencies import CurrentContext

from playmcp_viewer.config import DIContainer, Settings

from playmcp_viewer.inbound.dto import PlayMCPServer
from playmcp_viewer.outbound.client import get_playmcp_list
from playmcp_viewer.outbound.dto import PlaymcpListContentResponse, PlaymcpListResponse

settings = Settings()
mcp: FastMCP = DIContainer().mcp()


async def find_mcp_servers(
    cond: Literal["TOOTAL_TOOL_CALL_COUNT", "FEATURED_LEVEL", "CREATED_AT"],
    order_by: Literal["asc", "desc"],
    top_n: int,
    ctx: Context = CurrentContext(),
) -> list[PlayMCPServer]:
    """
    Retrieve a list of MCP servers registered on the Kakao PlayMCP platform, sorted by the specified condition and order.

    Tool Parameters:
        cond: The field to sort by. One of "TOOTAL_TOOL_CALL_COUNT", "FEATURED_LEVEL", or "CREATED_AT".
        order_by: Sorting direction. Must be "asc" for ascending or "desc" for descending.
        top_n: Number of top MCP servers to return.

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
        await ctx.info(
            f"search {page} page",
            extra={"page": page, "cond": cond, "order_by": order_by},
        )
        await ctx.report_progress(progress=len(playmcp_contents))

        playmcp_resp: PlaymcpListResponse = await get_playmcp_list(
            trace_id=ctx.request_id,
            page=page,
            sort_by=cond,
        )

        playmcp_contents.extend(playmcp_resp.content)

        if page + 1 == playmcp_resp.total_pages:
            break
        page += 1

    await ctx.report_progress(
        progress=len(playmcp_contents),
        total=len(playmcp_contents),
    )

    await ctx.info(
        f"sort searched servers by {order_by} direction",
        extra={
            "cond": cond,
            "order_by": order_by,
        },
    )
    if order_by == "asc":
        playmcp_contents = playmcp_contents[::-1]

    await ctx.info(
        f"filter searched servers by {top_n} count",
        extra={
            "cond": cond,
            "order_by": order_by,
            "top_n": top_n,
        },
    )
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
