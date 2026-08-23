from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Usage:
    tokens_in: int | None = None
    tokens_out: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> Usage | None:
        if not data:
            return None
        return cls(
            tokens_in=data.get("tokens_in") or data.get("tokensIn"),
            tokens_out=data.get("tokens_out") or data.get("tokensOut"),
        )


@dataclass
class ChatMessage:
    role: str
    content: str | list[Any] | dict[str, Any] | None = None
    tool_calls: list[dict[str, Any]] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> ChatMessage:
        if not data:
            return cls(role="assistant", content="")
        return cls(
            role=str(data.get("role", "assistant")),
            content=data.get("content"),
            tool_calls=data.get("tool_calls"),
        )

    @property
    def text(self) -> str:
        if isinstance(self.content, str):
            return self.content
        if isinstance(self.content, list):
            parts: list[str] = []
            for item in self.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(str(item.get("text", "")))
            return "".join(parts)
        return ""


@dataclass
class ChatChoice:
    finish_reason: str | None
    message: ChatMessage
    matched_stop: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChatChoice:
        return cls(
            finish_reason=data.get("finish_reason"),
            message=ChatMessage.from_dict(data.get("message")),
            matched_stop=data.get("matched_stop"),
        )


@dataclass
class ChatCompletion:
    success: bool
    message: str
    model: str
    created: str
    object: str
    choices: list[ChatChoice]
    usage: Usage | None = None
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ChatCompletion:
        data = payload.get("data") or {}
        request_items = data.get("request") or []
        choices = [ChatChoice.from_dict(item) for item in request_items]
        return cls(
            success=bool(payload.get("success")),
            message=str(payload.get("message", "")),
            model=str(data.get("model", "")),
            created=str(data.get("created", "")),
            object=str(data.get("object", "")),
            choices=choices,
            usage=Usage.from_dict(data.get("usage")),
            raw=payload,
        )

    @property
    def text(self) -> str:
        if not self.choices:
            return ""
        return self.choices[0].message.text


@dataclass
class ChatStreamChunk:
    """A single chunk from a streaming chat completion."""

    success: bool
    message: str
    delta: str
    role: str | None = None
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ChatStreamChunk:
        data = payload.get("data") or {}
        message_data = data.get("message") or {}
        content = message_data.get("content", "")
        delta = content if isinstance(content, str) else ChatMessage.from_dict(message_data).text
        return cls(
            success=bool(payload.get("success")),
            message=str(payload.get("message", "")),
            delta=delta,
            role=message_data.get("role"),
            raw=payload,
        )
