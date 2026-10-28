from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class QueueEntry:
    member_id: int
    joined_at: float
    status: str = "queued"


class MatchmakingService:
    """Safe abstraction for 1v1 queue and match creation.

    The current implementation intentionally uses a manual fallback and does not
    fabricate unsupported XPLAY.GG automated lobby endpoints.
    """

    def __init__(self):
        self.queue: dict[int, QueueEntry] = {}
        self.matches: dict[str, dict] = {}

    async def join_queue(self, member_id: int) -> dict:
        if member_id in self.queue:
            return {"status": "already_queued", "member_id": member_id}
        self.queue[member_id] = QueueEntry(member_id=member_id, joined_at=0)
        return {"status": "queued", "member_id": member_id}

    async def leave_queue(self, member_id: int) -> dict:
        self.queue.pop(member_id, None)
        return {"status": "removed", "member_id": member_id}

    async def try_match(self, member_a: int, member_b: int) -> dict:
        if member_a == member_b:
            return {"status": "invalid", "reason": "cannot_match_self"}
        match_id = f"manual-{min(member_a, member_b)}-{max(member_a, member_b)}"
        self.matches[match_id] = {
            "match_id": match_id,
            "players": [member_a, member_b],
            "status": "pending_manual_confirmation",
            "provider": "manual_fallback",
        }
        return self.matches[match_id]

    async def get_match_status(self, match_id: str) -> dict:
        return self.matches.get(match_id, {"status": "not_found", "match_id": match_id})

    async def submit_result(self, match_id: str, winner_id: int, loser_id: int) -> dict:
        match = self.matches.get(match_id)
        if not match:
            return {"status": "not_found", "match_id": match_id}
        match["status"] = "completed"
        match["winner_id"] = winner_id
        match["loser_id"] = loser_id
        match["verification_method"] = "manual_confirmation"
        return match
