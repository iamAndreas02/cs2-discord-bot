from __future__ import annotations


def build_rank_history(entries: list[dict]) -> str:
    if not entries:
        return "No historical Premier rating data is available yet."
    lines = ["Premier rank history", "--------------------"]
    for entry in entries[:10]:
        lines.append(f"{entry.get('captured_at', 'unknown')} :: {entry.get('rating', 'N/A')} ({entry.get('bracket', 'Unknown')})")
    return "\n".join(lines)
