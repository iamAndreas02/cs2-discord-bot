from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DiscordMember(Base):
    __tablename__ = "discord_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer, index=True)
    username: Mapped[str] = mapped_column(String(100))
    discriminator: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    steam_link: Mapped["SteamLink | None"] = relationship(back_populates="member")
    faceit_link: Mapped["FaceitLink | None"] = relationship(back_populates="member")
    premier_history: Mapped[list["PremierRatingHistory"]] = relationship(back_populates="member")
    match_participations: Mapped[list["MatchParticipant"]] = relationship(back_populates="member")


class SteamLink(Base):
    __tablename__ = "steam_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("discord_members.id"), unique=True, index=True)
    steam_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    steam_profile_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(32), default="pending")
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    member: Mapped[DiscordMember] = relationship(back_populates="steam_link")


class FaceitLink(Base):
    __tablename__ = "faceit_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("discord_members.id"), unique=True, index=True)
    faceit_id: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True)
    username: Mapped[str | None] = mapped_column(String(128), nullable=True)
    profile_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_without_faceit: Mapped[bool] = mapped_column(Boolean, default=False)
    last_refresh_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    member: Mapped[DiscordMember] = relationship(back_populates="faceit_link")


class PremierRatingHistory(Base):
    __tablename__ = "premier_rating_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("discord_members.id"), index=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bracket: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source: Mapped[str] = mapped_column(String(80), default="unknown")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)

    member: Mapped[DiscordMember] = relationship(back_populates="premier_history")


class MatchRecord(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_match_id: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True)
    provider: Mapped[str] = mapped_column(String(50), default="xplay")
    status: Mapped[str] = mapped_column(String(32), default="pending")
    winner_member_id: Mapped[int | None] = mapped_column(ForeignKey("discord_members.id"), nullable=True)
    loser_member_id: Mapped[int | None] = mapped_column(ForeignKey("discord_members.id"), nullable=True)
    result_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_method: Mapped[str | None] = mapped_column(String(64), nullable=True)
    dispute_status: Mapped[str] = mapped_column(String(32), default="none")
    match_link: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    participants: Mapped[list["MatchParticipant"]] = relationship(back_populates="match")


class MatchParticipant(Base):
    __tablename__ = "match_participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("discord_members.id"), index=True)
    steam_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    result_status: Mapped[str] = mapped_column(String(32), default="pending")
    joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    match: Mapped[MatchRecord] = relationship(back_populates="participants")
    member: Mapped[DiscordMember] = relationship(back_populates="match_participations")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_member_id: Mapped[int | None] = mapped_column(ForeignKey("discord_members.id"), nullable=True)
    target_member_id: Mapped[int | None] = mapped_column(ForeignKey("discord_members.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(120))
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
