from __future__ import annotations

from app.config import settings

BRACKET_TO_ROLE_ID = {
    "0-5000": 5000,
    "5001-10000": 10000,
    "10001-15000": 15000,
    "15001-20000": 20000,
    "20001-25000": 25000,
    "25001-30000": 30000,
    "30001+": 30001,
}


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
    for entry in entries[:10]:
        lines.append(f"{entry.get('captured_at', 'unknown')} :: {entry.get('rating', 'N/A')} ({entry.get('bracket', 'Unknown')})")
    return "\n".join(lines)


def get_role_for_bracket(bracket: str) -> int | None:
    normalized = bracket.replace("–", "-")
    return BRACKET_TO_ROLE_ID.get(normalized, None)


def sync_member_roles(member, guild, rating: int | None = None) -> None:
    if rating is None:
        return
    bracket, _, _ = get_bracket_for_rating(rating)
    role_id = get_role_for_bracket(bracket)
    if role_id is None:
        return
    role = guild.get_role(role_id)
    if role is not None:
        try:
            if role not in member.roles:
                guild.get_member(member.id).add_roles(role)
        except Exception:
            pass
