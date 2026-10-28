from __future__ import annotations

import httpx


class FaceitService:
    """Thin wrapper around official FACEIT API endpoints."""

    def __init__(self, api_key: str | None):
        self.api_key = api_key

    async def get_player(self, faceit_id: str) -> dict | None:
        if not self.api_key:
            raise RuntimeError("FACEIT_API_KEY not configured")

        url = f"https://open.faceit.com/data/v4/players/{faceit_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                return None
            return resp.json()

    async def get_player_by_name(self, nickname: str) -> dict | None:
        if not self.api_key:
            raise RuntimeError("FACEIT_API_KEY not configured")

        url = "https://open.faceit.com/data/v4/search/players"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"nickname": nickname}
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers=headers, params=params)
            if resp.status_code != 200:
                return None
            data = resp.json()
            items = data.get("items") or []
            return items[0] if items else None

    @staticmethod
    def get_summary(player_payload: dict | None) -> dict:
        if not player_payload:
            return {
                "status": "unlinked",
                "level": None,
                "elo": None,
                "nickname": None,
            }

        return {
            "status": "linked",
            "level": player_payload.get("games", {}).get("cs2", {}).get("skill_level"),
            "elo": player_payload.get("games", {}).get("cs2", {}).get("faceit_elo"),
            "nickname": player_payload.get("nickname"),
        }
