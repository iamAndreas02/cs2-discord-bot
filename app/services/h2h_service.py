from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AuditEntry:
    action: str
    details: str
    actor_id: int | None = None
    target_id: int | None = None


class AuditService:
    def __init__(self):
        self.entries: list[AuditEntry] = []

    def record(self, action: str, details: str, actor_id: int | None = None, target_id: int | None = None) -> AuditEntry:
        entry = AuditEntry(action=action, details=details, actor_id=actor_id, target_id=target_id)
        self.entries.append(entry)
        return entry

    def recent(self, limit: int = 10) -> list[str]:
        recent = self.entries[-limit:]
        return [f"{item.action}: {item.details}" for item in recent]
