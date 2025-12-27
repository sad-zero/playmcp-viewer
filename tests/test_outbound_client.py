import uuid

import pytest

from playmcp_viewer.outbound.client import get_playmcp_list
from playmcp_viewer.outbound.dto import PlaymcpListContentResponse, PlaymcpListResponse


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sort_by", ["CREATED_AT", "FEATURED_LEVEL", "TOTAL_TOOL_CALL_COUNT"]
)
async def test_get_playmcp_list(sort_by: str):
    # given
    trace_id = uuid.uuid4()

    # when
    page = 0
    total_contents: list[PlaymcpListContentResponse] = []
    while True:
        resp: PlaymcpListResponse = await get_playmcp_list(
            trace_id=trace_id,
            sort_by=sort_by,
            page=page,
        )
        assert resp.page == page

        total_contents.extend(resp.content)

        if resp.page + 1 == resp.total_pages:
            break
        else:
            page = page + 1
    # then
    assert len(total_contents) == resp.total_elements
