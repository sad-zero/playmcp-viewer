import httpx
import logging
from typing import Literal

from playmcp_viewer.config import Settings
from playmcp_viewer.outbound.dto import PlaymcpListResponse

settings = Settings()

logger = logging.getLogger("playmcp_viewer.outbound")


async def get_playmcp_list(
    trace_id: str,
    sort_by: Literal["TOOTAL_TOOL_CALL_COUNT", "FEATURED_LEVEL", "CREATED_AT"],
    page: int = 0,
) -> list[PlaymcpListResponse]:
    params = {
        "page": page,
        "pageSize": 12,
        "sortBy": sort_by,
    }
    path = "/mcps"
    async with httpx.AsyncClient(base_url=settings.kakao_playmcp_endpoint) as client:
        client_resp = await client.get(url=path, params=params)
        if client_resp.is_success:
            logger.info(
                "request successes",
                extra={
                    "trace_id": trace_id,
                    "base_url": settings.kakao_playmcp_endpoint,
                    "path": path,
                    "params": params,
                },
            )
        else:
            logger.warning(
                "request fails",
                extra={
                    "trace_id": trace_id,
                    "base_url": settings.kakao_playmcp_endpoint,
                    "path": path,
                    "params": params,
                },
            )
            return []

        resp = PlaymcpListResponse.model_validate(client_resp.json())
    logger.info(
        "response is converted",
        extra={
            "trace_id": trace_id,
            "response": resp,
        },
    )
    return resp
