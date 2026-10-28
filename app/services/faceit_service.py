from __future__ import annotations

from urllib.parse import urlencode


class SteamOpenIDService:
    """Handles the official Steam OpenID verification flow.

    This service intentionally does not claim to provide Premier rating data from Steam.
    It only verifies account ownership via the official OpenID mechanism.
    """

    def build_auth_url(self, *, realm: str, return_to: str, state: str) -> str:
        params = {
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "openid.mode": "checkid_setup",
            "openid.return_to": return_to,
            "openid.realm": realm,
            "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
            "state": state,
        }
        return "https://steamcommunity.com/openid/login?" + urlencode(params)

    async def verify_openid_response(self, payload: dict) -> str | None:
        """Validate the callback and return a 64-bit Steam ID if valid.

        In production, this should validate the OpenID response against Steam's endpoint.
        This placeholder is intentionally minimal and safe.
        """
        claimed_id = payload.get("openid.claimed_id") or payload.get("claimed_id")
        if not claimed_id:
            return None
        if "steamcommunity.com/openid/id/" not in claimed_id:
            return None
        return claimed_id.rsplit("/", 1)[-1]
