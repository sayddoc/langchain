"""Shared memory primitives for inter-agent state exchange."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any


@dataclass(slots=True)
class SharedMemory:
    """Thread-safe in-memory key-value store for agent collaboration."""

    _state: dict[str, Any] = field(default_factory=dict)
    _lock: Lock = field(default_factory=Lock)

    def write(self, key: str, value: Any) -> None:
        """Store an object by key."""
        with self._lock:
            self._state[key] = value

    def read(self, key: str, default: Any = None) -> Any:
        """Read an object by key."""
        with self._lock:
            return self._state.get(key, default)

    def snapshot(self) -> dict[str, Any]:
        """Return a defensive copy of the full memory state."""
        with self._lock:
            return dict(self._state)
