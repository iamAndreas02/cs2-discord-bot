from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class VerificationRecord:
    member_id: int
    steam_id: str | None = None
    verified: bool = False
    verified_at: datetime | None = None
    last_attempt_at: datetime | None = None
    attempts: int = 0


class VerificationService:
    """Persistent-style verifier for Steam ownership and cooldown checks."""

    def __init__(self):
        self.records: dict[int, VerificationRecord] = {}

    def get_record(self, member_id: int) -> VerificationRecord:
        record = self.records.get(member_id)
        if record is None:
            record = VerificationRecord(member_id=member_id)
            self.records[member_id] = record
        return record

    def set_steam_id(self, member_id: int, steam_id: str) -> VerificationRecord:
        record = self.get_record(member_id)
        record.steam_id = steam_id
        record.verified = True
        record.verified_at = datetime.utcnow()
        return record

    def can_attempt(self, member_id: int, cooldown_seconds: int = 180) -> tuple[bool, str]:
        record = self.get_record(member_id)
        now = datetime.utcnow()
        if record.last_attempt_at and now - record.last_attempt_at < timedelta(seconds=cooldown_seconds):
            return False, "Verification has a cooldown. Please wait before trying again."
        return True, "OK"

    def register_attempt(self, member_id: int) -> VerificationRecord:
        record = self.get_record(member_id)
        record.attempts += 1
        record.last_attempt_at = datetime.utcnow()
        return record

    def is_verified(self, member_id: int) -> bool:
        return self.get_record(member_id).verified

    def revoke_verification(self, member_id: int) -> VerificationRecord:
        record = self.get_record(member_id)
        record.verified = False
        record.steam_id = None
        record.verified_at = None
        return record
