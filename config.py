import os, json
from pydantic import BaseModel

class Settings(BaseModel):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    GROUP_ID: int = int(os.getenv("GROUP_ID", "-1"))
    VIP_GROUP_ID: int = int(os.getenv("VIP_GROUP_ID", "-1"))
    TIMEZONE: str = os.getenv("TIMEZONE", "America/Sao_Paulo")
    INTERVAL_HOURS: int = int(os.getenv("INTERVAL_HOURS", "6"))
    MEDIA_DIR: str | None = os.getenv("MEDIA_DIR")
    MEDIA_URLS: list[str] | None = json.loads(os.getenv("MEDIA_URLS_JSON", "[]") or "[]")
    CHECKOUT_URL_TMPL: str = os.getenv("CHECKOUT_URL_TMPL", "")
    GATEWAY_WEBHOOK_SECRET: str = os.getenv("GATEWAY_WEBHOOK_SECRET", "")
    PUBLIC_BASE_URL: str = os.getenv("PUBLIC_BASE_URL", "")

settings = Settings()
