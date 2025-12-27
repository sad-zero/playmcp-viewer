from typing import Annotated

from pydantic import BaseModel, ConfigDict, BeforeValidator, Field
from pydantic.alias_generators import to_camel


class PlaymcpListResponse(BaseModel):
    model_config = ConfigDict(frozen=True, alias_generator=to_camel)

    page: int
    total_pages: int
    total_elements: Annotated[int, BeforeValidator(int)]
    content: list["PlaymcpListContentResponse"]


class PlaymcpListContentResponse(BaseModel):
    model_config = ConfigDict(frozen=True, alias_generator=to_camel)

    id: str
    name: str
    description: str
    status: str
    starter_messages: list[str]
    formatted_tools: list["PlaymcpListFormattedTool"]
    monthly_tool_call_count: Annotated[int, BeforeValidator(int)]
    total_tool_call_count: Annotated[int, BeforeValidator(int)]
    identify_name: str
    applicable_ai_service_scope: str = Field(alias="applicableAIServiceScope")
    featured_level: int
    image: "PlaymcpListContentImage"
    developer_name: str
    auth_config_summary: dict


class PlaymcpListFormattedTool(BaseModel):
    model_config = ConfigDict(frozen=True, alias_generator=to_camel)

    name: str
    description: str
    parameters: list["PlaymcpListFormattedToolParameter"]


class PlaymcpListFormattedToolParameter(BaseModel):
    model_config = ConfigDict(frozen=True, alias_generator=to_camel)

    name: str
    type: str
    description: str | None
    required: bool


class PlaymcpListContentImage(BaseModel):
    model_config = ConfigDict(frozen=True, alias_generator=to_camel)

    path: str
    full_url: str
    cdn_url: str
