from __future__ import annotations


def get_mock_premier_leaderboard() -> list[dict]:
    return [
        {"rank": 1, "player": "Nexus", "rating": 29650, "bracket": "30,001+"},
        {"rank": 2, "player": "Kiro", "rating": 24080, "bracket": "20,001–25,000"},
        {"rank": 3, "player": "Milo", "rating": 18750, "bracket": "15,001–20,000"},
        {"rank": 4, "player": "Vex", "rating": 12480, "bracket": "10,001–15,000"},
        {"rank": 5, "player": "Rook", "rating": 8600, "bracket": "5,001–10,000"},
    ]


def generate_leaderboard_message() -> str:
    lines = ["Premier leaderboard", "------------------"]
    for entry in get_mock_premier_leaderboard():
        lines.append(
            f"#{entry['rank']} {entry['player']} — {entry['rating']} ({entry['bracket']})"
        )
    return "\n".join(lines)
