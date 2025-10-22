import asyncio
import os
from itertools import count

from fastapi import FastAPI
import uvicorn
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings
from media import iter_media_files, send_media
from utils import setup_logger

logger = setup_logger("bot_vip")

# ---- HTTP (para o Render detectar porta) ----
app = FastAPI()

@app.get("/")
@app.get("/health")
def health():
    return {"ok": True, "service": "bot_vip"}

# ---- Mensageria ----
MSG = "🔞 Conteúdo VIP liberado! Aproveite!"
CAPTION = MSG
_counter = count(0)

async def tick(ptb_app: Application):
    bot = ptb_app.bot
    if settings.GROUP_ID < 0:
        logger.error("GROUP_ID inválido (VIP). Defina a env GROUP_ID.")
        return

    local = iter_media_files(settings.MEDIA_DIR) if settings.MEDIA_DIR else []
    urls = settings.MEDIA_URLS or []
    pool = local + urls

    if not pool:
        await bot.send_message(chat_id=settings.GROUP_ID, text=MSG)
        logger.info("Enviado texto VIP (sem mídia).")
        return

    idx = next(_counter) % len(pool)
    item = pool[idx]
    await send_media(bot, settings.GROUP_ID, item, caption=CAPTION)
    logger.info(f"VIP enviado: {item} (idx={idx})")

async def _run():
    ptb = Application.builder().token(settings.BOT_TOKEN).build()
    await ptb.initialize()
    await ptb.bot.delete_webhook(drop_pending_updates=True)

    scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)
    scheduler.add_job(lambda: asyncio.create_task(tick(ptb)),
                      "interval", hours=settings.INTERVAL_HOURS)
    scheduler.start()
    logger.info("Scheduler iniciado (VIP) — com endpoint /health.")

    await ptb.start()

    port = int(os.getenv("PORT", "10000"))
    server = uvicorn.Server(uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info"))
    await server.serve()

def main():
    asyncio.run(_run())
