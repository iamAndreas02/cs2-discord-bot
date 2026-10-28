from __future__ import annotations

from app.providers.base_provider import MatchmakingProvider


class XplayProvider(MatchmakingProvider):
    """Provider abstraction for XPLAY.GG.

    This intentionally does not fabricate unsupported automation endpoints.
    The implementation remains safe and should only be enabled after official,
    documented support exists.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def queue_member(self, member_id: int, payload: dict) -> dict:
        return {
            "status": "unsupported",
            "message": "XPLAY.GG automated queueing is not currently supported by the official integration contract.",
            "member_id": member_id,
            "payload": payload,
        }

    async def dequeue_member(self, member_id: int) -> dict:
        return {"status": "ok", "member_id": member_id, "removed": True}

    async def create_or_join_match(self, player_a_id: int, player_b_id: int) -> dict:
        return {
            "status": "unsupported",
            "message": "No official XPLAY.GG match creation endpoint was confirmed for this implementation.",
            "players": [player_a_id, player_b_id],
        }

    async def get_match_status(self, match_id: str) -> dict:
        return {"status": "unknown", "match_id": match_id}

    async def submit_result(self, match_id: str, result: dict) -> dict:
        return {"status": "manual_fallback", "match_id": match_id, "result": result}
