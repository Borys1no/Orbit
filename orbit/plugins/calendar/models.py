"""Calendar models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class EventData:
    event_id: str
    summary: str
    description: str
    start: str
    end: str
    location: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "summary": self.summary,
            "description": self.description,
            "start": self.start,
            "end": self.end,
            "location": self.location,
        }
