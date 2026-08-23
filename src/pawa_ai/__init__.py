"""Pawa AI Python SDK."""

from pawa_ai._client import AsyncPawaAI, PawaAI
from pawa_ai._exceptions import (
    APIConnectionError,
    APIError,
    APIStatusError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    PawaAIError,
    RateLimitError,
)
from pawa_ai._retry import RetryConfig
from pawa_ai._streaming import AsyncChatCompletionStream, ChatCompletionStream
from pawa_ai.models import (
    APIResponse,
    ChatCompletion,
    ChatMessage,
    ChatStreamChunk,
    EmbeddingResponse,
    Model,
    ModelList,
    Usage,
)

__all__ = [
    "PawaAI",
    "AsyncPawaAI",
    "RetryConfig",
    "ChatCompletionStream",
    "AsyncChatCompletionStream",
    "APIResponse",
    "ChatCompletion",
    "ChatMessage",
    "ChatStreamChunk",
    "EmbeddingResponse",
    "Model",
    "ModelList",
    "Usage",
    "PawaAIError",
    "APIError",
    "APIConnectionError",
    "APIStatusError",
    "AuthenticationError",
    "BadRequestError",
    "NotFoundError",
    "RateLimitError",
]

__version__ = "0.2.0"
