from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Model:
    id: int | None = None
    name: str | None = None
    model_type: str | None = None
    description: str | None = None
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Model:
        return cls(
            id=data.get("id"),
            name=data.get("name") or data.get("modelName"),
            model_type=data.get("modelType") or data.get("type"),
            description=data.get("description"),
            raw=data,
        )


@dataclass
class ModelList:
    success: bool
    message: str
    models: list[Model]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ModelList:
        data = payload.get("data")
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get("models") or data.get("items") or data.get("data") or []
        else:
            items = []

        return cls(
            success=bool(payload.get("success")),
            message=str(payload.get("message", "")),
            models=[Model.from_dict(item) for item in items if isinstance(item, dict)],
            raw=payload,
        )
