from __future__ import annotations

from app.config import settings

PREMIER_BRACKETS = [
    ("Unranked / rating unavailable", None, None),
    ("0–5,000", 0, 5000),
    ("5,001–10,000", 5001, 10000),
    ("10,001–15,000", 10001, 15000),
    ("15,001–20,000", 15001, 20000),
    ("20,001–25,000", 20001, 25000),
    ("25,001–30,000", 25001, 30000),
    ("30,001+", 30001, None),
]


def get_rating_bracket(rating: int | None) -> tuple[str, int | None, int | None]:
    if rating is None:
        return PREMIER_BRACKETS[0]

    for label, min_value, max_value in PREMIER_BRACKETS[1:]:
        if max_value is None:
            if rating >= min_value:
                return label, min_value, max_value
        elif min_value <= rating <= max_value:
            return label, min_value, max_value

    return PREMIER_BRACKETS[0]


def bracket_to_role_id(rating: int | None) -> int | None:
    bracket_name, _, _ = get_rating_bracket(rating)
    if bracket_name == "Unranked / rating unavailable":
        return None

    mapping = settings.rank_role_brackets
    normalized = {
        "0-5000": 5000,
        "5001-10000": 10000,
        "10001-15000": 15000,
        "15001-20000": 20000,
        "20001-25000": 25000,
        "25001-30000": 30000,
        "30001+": 30001,
    }

    role_value = normalized.get(bracket_name.replace("–", "-").replace("+", "+"), 0)
    return role_value


def get_role_name_for_rating(rating: int | None) -> str:
    label, _, _ = get_rating_bracket(rating)
    return label
