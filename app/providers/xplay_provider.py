from __future__ import annotations


class MatchmakingProvider:
    async def queue_member(self, member_id: int, payload: dict) -> dict:
        raise NotImplementedError

    async def dequeue_member(self, member_id: int) -> dict:
        raise NotImplementedError

    async def create_or_join_match(self, player_a_id: int, player_b_id: int) -> dict:
        raise NotImplementedError

    async def get_match_status(self, match_id: str) -> dict:
        raise NotImplementedError

    async def submit_result(self, match_id: str, result: dict) -> dict:
        raise NotImplementedError
