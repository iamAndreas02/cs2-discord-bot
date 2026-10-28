from __future__ import annotations


def get_rating_bracket(rating: int | None) -> tuple[str, int | None, int | None]:
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

    for label, min_value, max_value in ranges:
        if max_value is None:
            if rating >= min_value:
                return label, min_value, max_value
        elif min_value <= rating <= max_value:
            return label, min_value, max_value

    return ("Unranked / rating unavailable", None, None)
