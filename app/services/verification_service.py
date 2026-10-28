from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class VerificationRecord:
    member_id: int
    steam_id: str | None = None
    verified: bool = False
    verified_at: datetime | None = None
    last_attempt_at: datetime | None = None
    attempts: int = 0
    attempts_last_hour: int = 0
    last_attempt_hour_start: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "member_id": self.member_id,
            "steam_id": self.steam_id,
            "verified": self.verified,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "last_attempt_at": self.last_attempt_at.isoformat() if self.last_attempt_at else None,
            "attempts": self.attempts,
            "attempts_last_hour": self.attempts_last_hour,
            "last_attempt_hour_start": self.last_attempt_hour_start.isoformat() if self.last_attempt_hour_start else None,
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "VerificationRecord":
        def parse_time(value: str | None):
            if not value:
                return None
            return datetime.fromisoformat(value)

        return cls(
            member_id=int(payload.get("member_id", 0)),
            steam_id=payload.get("steam_id"),
            verified=bool(payload.get("verified", False)),
            verified_at=parse_time(payload.get("verified_at")),
            last_attempt_at=parse_time(payload.get("last_attempt_at")),
            attempts=int(payload.get("attempts", 0)),
            attempts_last_hour=int(payload.get("attempts_last_hour", 0)),
            last_attempt_hour_start=parse_time(payload.get("last_attempt_hour_start")),
        )


class VerificationService:
    """Verification state with disk persistence, cooldown enforcement, and rejoin-safe records."""

    def __init__(self, storage_path: str | None = None):
        self.storage_path = Path(storage_path or "data/verification_state.json")
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.records: dict[int, VerificationRecord] = self._load()

    def _load(self) -> dict[int, VerificationRecord]:
        if not self.storage_path.exists():
            return {}
        try:
            with self.storage_path.open("r", encoding="utf-8") as handle:
                raw = json.load(handle)
        except (json.JSONDecodeError, OSError):
            return {}

        records: dict[int, VerificationRecord] = {}
        for value in raw.values():
            record = VerificationRecord.from_dict(value)
            records[record.member_id] = record
        return records

    def _save(self) -> None:
        payload = {str(member_id): record.to_dict() for member_id, record in self.records.items()}
        with self.storage_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def get_record(self, member_id: int) -> VerificationRecord:
        record = self.records.get(member_id)
        if record is None:
            record = VerificationRecord(member_id=member_id)
            self.records[member_id] = record
            self._save()
        return record

    def set_steam_id(self, member_id: int, steam_id: str) -> VerificationRecord:
        record = self.get_record(member_id)
        record.steam_id = steam_id
        record.verified = True
        record.verified_at = datetime.utcnow()
        self._save()
        return record

    def can_attempt(self, member_id: int, cooldown_seconds: int = 180, max_attempts_per_hour: int = 10) -> tuple[bool, str]:
        record = self.get_record(member_id)
        now = datetime.utcnow()

        if record.last_attempt_at and now - record.last_attempt_at < timedelta(seconds=cooldown_seconds):
            return False, "Verification has a cooldown. Please wait before trying again."

        if record.last_attempt_hour_start is None:
            record.last_attempt_hour_start = now
            record.attempts_last_hour = 0

        if record.last_attempt_hour_start and now - record.last_attempt_hour_start >= timedelta(hours=1):
            record.last_attempt_hour_start = now
            record.attempts_last_hour = 0

        if record.attempts_last_hour >= max_attempts_per_hour:
            return False, "You have reached the hourly verification limit. Please try again later."

        return True, "OK"

    def register_attempt(self, member_id: int) -> VerificationRecord:
        record = self.get_record(member_id)
        record.attempts += 1
        now = datetime.utcnow()
        record.last_attempt_at = now

        if record.last_attempt_hour_start is None or now - record.last_attempt_hour_start >= timedelta(hours=1):
            record.last_attempt_hour_start = now
            record.attempts_last_hour = 0

        record.attempts_last_hour += 1
        self._save()
        return record

    def is_verified(self, member_id: int) -> bool:
        return self.get_record(member_id).verified

    def revoke_verification(self, member_id: int) -> VerificationRecord:
        record = self.get_record(member_id)
        record.verified = False
        record.steam_id = None
        record.verified_at = None
        self._save()
        return record

    def mark_verified(self, member_id: int, steam_id: str) -> VerificationRecord:
        record = self.get_record(member_id)
        record.steam_id = steam_id
        record.verified = True
        record.verified_at = datetime.utcnow()
        self._save()
        return record

    def reset_for_rejoin(self, member_id: int) -> VerificationRecord:
        record = self.get_record(member_id)
        record.verified = False
        record.steam_id = None
        record.verified_at = None
        record.last_attempt_at = None
        record.attempts_last_hour = 0
        record.last_attempt_hour_start = None
        self._save()
        return record
