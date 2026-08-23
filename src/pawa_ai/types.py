from __future__ import annotations

from typing import Any, Literal, TypedDict


class TextContent(TypedDict):
    type: Literal["text"]
    text: str


class ImageURL(TypedDict):
    url: str


class ImageContent(TypedDict):
    type: Literal["image_url"]
    image_url: ImageURL


ContentPart = TextContent | ImageContent


class ChatMessage(TypedDict, total=False):
    role: Literal["system", "user", "assistant", "tool"]
    content: str | list[ContentPart]
    name: str
    tool_call_id: str
    tool_calls: list[dict[str, Any]]


class ToolFunction(TypedDict, total=False):
    name: str
    description: str
    strict: bool
    parameters: dict[str, Any]


class Tool(TypedDict):
    type: Literal["function"]
    function: ToolFunction


class ResponseFormat(TypedDict, total=False):
    type: Literal["json_schema", "text"]
    json_schema: dict[str, Any]


class ReasoningConfig(TypedDict, total=False):
    effort: Literal["low", "medium", "high"]


class RAGConfig(TypedDict, total=False):
    knowledgeBaseId: int
    topK: int


class ChatRequest(TypedDict, total=False):
    model: str
    messages: list[ChatMessage]
    temperature: float
    top_p: float
    max_tokens: int
    frequency_penalty: float
    presence_penalty: float
    seed: int
    stream: bool
    tools: list[Tool]
    tool_choice: str | dict[str, Any]
    response_format: ResponseFormat
    reasoning: ReasoningConfig
    rag: RAGConfig
    memoryChat: list[ChatMessage]
    agents: list[int]


class TextToSpeechRequest(TypedDict, total=False):
    text: str
    voice: Literal["ame", "liora", "ayana"]
    model: str
    max_tokens: int
    temperature: float
    top_p: float


class EmbeddingRequest(TypedDict, total=False):
    model: str
    sentences: list[str]
    lang: str


class CreateAgentRequest(TypedDict, total=False):
    name: str
    description: str
    instruction: str
    intents: list[str]
    knowledgeBaseId: int
    tools: list[Tool]


class AgentChatRequest(TypedDict, total=False):
    name: str
    description: str
    instruction: str
    intents: list[str]
    model: str
    message: ChatMessage
    agents: list[int]
    memoryChat: list[ChatMessage]
    temperature: float
    top_p: float
    max_tokens: int
    frequency_penalty: float
    presence_penalty: float
    seed: int
    reasoning: ReasoningConfig
    stream: bool
    response_format: ResponseFormat


class KnowledgeBaseCreateRequest(TypedDict, total=False):
    name: str
    description: str


class SemanticRetrievalRequest(TypedDict, total=False):
    knowledgeBaseId: int
    query: str
    topK: int


class WorkspaceCreateRequest(TypedDict, total=False):
    name: str
