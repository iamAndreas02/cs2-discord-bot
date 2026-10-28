from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, Base
from app.models.member import DiscordMember, FaceitLink, MatchParticipant, MatchRecord, PremierRatingHistory, SteamLink


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_member(self, member_id: int) -> DiscordMember | None:
        result = await self.session.execute(select(DiscordMember).where(DiscordMember.id == member_id))
        return result.scalar_one_or_none()

    async def upsert_member(self, member_id: int, guild_id: int, username: str, discriminator: str | None = None) -> DiscordMember:
        member = await self.get_member(member_id)
        if member is None:
            member = DiscordMember(id=member_id, guild_id=guild_id, username=username, discriminator=discriminator)
            self.session.add(member)
        else:
            member.guild_id = guild_id
            member.username = username
            member.discriminator = discriminator
        await self.session.commit()
        return member

    async def save_steam_link(self, member_id: int, steam_id: str, profile_url: str | None = None) -> SteamLink:
        stmt = select(SteamLink).where(SteamLink.member_id == member_id)
        result = await self.session.execute(stmt)
        link = result.scalar_one_or_none()
        if link is None:
            link = SteamLink(member_id=member_id, steam_id=steam_id, steam_profile_url=profile_url)
            self.session.add(link)
        else:
            link.steam_id = steam_id
            link.steam_profile_url = profile_url
        await self.session.commit()
        return link

    async def save_faceit_link(self, member_id: int, faceit_id: str | None, username: str | None, profile_url: str | None = None) -> FaceitLink:
        stmt = select(FaceitLink).where(FaceitLink.member_id == member_id)
        result = await self.session.execute(stmt)
        link = result.scalar_one_or_none()
        if link is None:
            link = FaceitLink(member_id=member_id, faceit_id=faceit_id, username=username, profile_url=profile_url)
            self.session.add(link)
        else:
            link.faceit_id = faceit_id
            link.username = username
            link.profile_url = profile_url
        await self.session.commit()
        return link

    async def save_premier_snapshot(self, member_id: int, rating: int | None, bracket: str | None, source: str = "manual") -> PremierRatingHistory:
        history = PremierRatingHistory(member_id=member_id, rating=rating, bracket=bracket, source=source, is_current=True)
        self.session.add(history)
        await self.session.commit()
        return history

    async def get_latest_ratings(self) -> list[dict[str, Any]]:
        stmt = select(PremierRatingHistory).order_by(PremierRatingHistory.created_at.desc())
        result = await self.session.execute(stmt)
        rows = result.scalars().all()
        return [
            {
                "member_id": r.member_id,
                "rating": r.rating,
                "bracket": r.bracket,
                "source": r.source,
                "created_at": r.created_at,
            }
            for r in rows
        ]


async def get_repository() -> Repository:
    session = AsyncSessionLocal()
    return Repository(session)
