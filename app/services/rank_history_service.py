from __future__ import annotations


def compute_h2h(member_a_id: int, member_b_id: int, matches: list[dict]) -> dict:
    total = 0
    wins_a = 0
    wins_b = 0
    draws = 0

    for match in matches:
        if match.get("status") != "completed" or not match.get("result_verified"):
            continue
        if match.get("winner_id") == member_a_id:
            wins_a += 1
        elif match.get("winner_id") == member_b_id:
            wins_b += 1
        else:
            draws += 1
        total += 1

    win_rate_a = (wins_a / total * 100) if total else 0.0
    return {
        "matches_played": total,
        "wins_a": wins_a,
        "wins_b": wins_b,
        "draws": draws,
        "win_rate_a": round(win_rate_a, 1),
        "leader": "Equal record" if wins_a == wins_b else ("Player A" if wins_a > wins_b else "Player B"),
    }
