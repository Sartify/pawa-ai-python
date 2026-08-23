from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmbeddingData:
    embeddings: list[list[float]]

    @classmethod
    def from_dict(cls, data: dict[str, Any] | list[Any] | None) -> EmbeddingData:
        if isinstance(data, list):
            return cls(embeddings=data)
        if not data:
            return cls(embeddings=[])
        return cls(embeddings=list(data.get("embeddings") or []))


@dataclass
class EmbeddingResponse:
    success: bool
    message: str
    embeddings: list[list[float]]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> EmbeddingResponse:
        data = EmbeddingData.from_dict(payload.get("data"))
        return cls(
            success=bool(payload.get("success")),
            message=str(payload.get("message", "")),
            embeddings=data.embeddings,
            raw=payload,
        )
