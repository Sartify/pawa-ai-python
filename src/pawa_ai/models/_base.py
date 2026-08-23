from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass
class APIResponse(Generic[T]):
    """Standard Pawa AI API envelope."""

    success: bool
    message: str
    data: T
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_dict(
        cls,
        payload: dict[str, Any],
        *,
        data_parser: Callable[[Any], T] | None = None,
    ) -> APIResponse[T]:
        data = payload.get("data")
        if data_parser is not None and data is not None:
            parsed_data = data_parser(data)
        else:
            parsed_data = data  # type: ignore[assignment]
        return cls(
            success=bool(payload.get("success")),
            message=str(payload.get("message", "")),
            data=parsed_data,
            raw=payload,
        )


def get_nested(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
    return current
