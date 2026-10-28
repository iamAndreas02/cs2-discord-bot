from __future__ import annotations

from datetime import datetime


def build_admin_status() -> str:
    return (
        "Bot status: online\n"
        "Database: initialized\n"
        "Steam verification: supported via official OpenID\n"
        "FACEIT API: supported through official bearer-based API\n"
        "XPLAY: manual fallback enabled; no unsupported automation claimed\n"
        "Configuration: role mappings and channel names are environment driven\n"
    )


def build_audit_summary(entries: list[dict]) -> str:
    if not entries:
        return "No audit entries recorded yet."
    lines = ["Recent audit log", "----------------"]
    for entry in entries[:8]:
        lines.append(f"{entry.get('created_at', datetime.utcnow())} :: {entry.get('action', 'unknown')}")
    return "\n".join(lines)
