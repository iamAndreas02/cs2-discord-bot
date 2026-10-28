from __future__ import annotations


def get_bracket_for_rating(rating: int | None) -> tuple[str, int | None, int | None]:
    if rating is None:
        return ("Unranked / rating unavailable", None, None)
    ranges = [
        ("0–5,000", 0, 5000),
        ("5,001–10,000", 5001, 10000),
        ("10,001–15,000", 10001, 15000),
        ("15,001–20,000", 15001, 20000),
        ("20,001–25,000", 20001, 25000),
        ("25,001–30,000", 25001, 30000),
        ("30,001+", 30001, None),
    ]
    for label, low, high in ranges:
        if high is None:
            if rating >= low:
                return label, low, high
        elif low <= rating <= high:
            return label, low, high
    return ("Unranked / rating unavailable", None, None)


def determine_role_from_rating(rating: int | None) -> str:
    bracket, _, _ = get_bracket_for_rating(rating)
    return bracket


def build_rank_history(entries: list[dict]) -> str:
    if not entries:
        return "No historical Premier rating data is available yet."
    lines = ["Premier rank history", "--------------------"]
    for e in entries[:10]:
        lines.append(f"{e.get('captured_at', 'unknown')} :: {e.get('rating', 'N/A')} ({e.get('bracket', 'Unknown')})")
    return "\n".join(lines)
