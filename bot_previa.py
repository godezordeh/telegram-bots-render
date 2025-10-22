import asyncio, os
from itertools import count
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from common.config import settings
from common.media import iter_media_files, send_media
from common.utils import setup_logger

logger = setup_logger("bot_previa")

MSG = "🔥 Prévia exclusiva! Quer ver tudo? Entre no VIP!"
CAPTION = MSG

_counter = count(0)  # index simples para round-robin

async def tick(app: Application):
    bot = app.bot
    if settings.GROUP_ID < 0:
        logger.error("GROUP_ID inválido (prévia). Defina a env GROUP_ID.")
        return

    local = iter_media_files(settings.MEDIA_DIR) if settings.MEDIA_DIR else []
    urls = settings.MEDIA_URLS or []
    pool = local + urls

    if not pool:
        await bot.send_message(chat_id=settings.GROUP_ID, text=MSG)
        logger.info("Enviado texto (sem mídia).")
        return

    idx = next(_counter) % len(pool)
    item = pool[idx]
    await send_media(bot, settings.GROUP_ID, item, caption=CAPTION)
    logger.info(f"Prévia enviada: {item} (idx={idx})")

def main():
    app = Application.builder().token(settings.BOT_TOKEN).build()
    scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)
    scheduler.add_job(lambda: asyncio.create_task(tick(app)), "interval", hours=settings.INTERVAL_HOURS)
    scheduler.start()
    logger.info("Scheduler iniciado (prévia).")
    app.run_polling(allowed_updates=[])
