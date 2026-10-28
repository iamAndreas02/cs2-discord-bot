from __future__ import annotations


def build_profile_message(member_id: int, display_name: str) -> str:
    return (
        f"Player profile for {display_name}\n"
        "-----------------------------------\n"
        f"Discord ID: {member_id}\n"
        "Steam: Not linked\n"
        "Premier rating: Unavailable\n"
        "Premier bracket: Unranked / rating unavailable\n"
        "FACEIT: Not linked\n"
        "Verification status: Pending\n"
        "Head-to-head: No recorded matches yet\n"
        "Last refresh: Never\n"
    )


def build_h2h_summary() -> str:
    return (
        "Head-to-Head\n"
        "------------\n"
        "No opponents recorded yet. Complete at least one verified 1v1 match to start tracking rivalry history."
    )
