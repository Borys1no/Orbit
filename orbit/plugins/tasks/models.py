"""Tasks models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class TaskData:
    task_id: str
    title: str
    notes: str
    status: str
    due: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "notes": self.notes,
            "status": self.status,
            "due": self.due,
        }
