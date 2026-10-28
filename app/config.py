from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "cs2-discord-bot"
    debug: bool = False
    discord_token: str = ""
    discord_guild_id: int = 0
    database_url: str = "sqlite+aiosqlite:///./cs2_bot.db"

    steam_openid_realm: str = "http://localhost:8000"
    steam_openid_return_to: str = "http://localhost:8000/auth/steam/callback"
    faceit_api_key: str | None = None
    xplay_api_key: str | None = None

    profile_channel_name: str = "🎮・my-profile"
    verification_cooldown_seconds: int = 180
    max_verification_attempts_per_hour: int = 10

    rank_role_brackets: dict[str, int] = {
        "0-5000": 5000,
        "5001-10000": 10000,
        "10001-15000": 15000,
        "15001-20000": 20000,
        "20001-25000": 25000,
        "25001-30000": 30000,
        "30001+": 30001,
    }


settings = Settings()
