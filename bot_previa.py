import asyncio
from itertools import count
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import settings
from media import iter_media_files, send_media
from utils import setup_logger

logger = setup_logger("bot_previa")

MSG = "🔥 Prévia exclusiva! Quer ver tudo? Entre no VIP!"
CAPTION = MSG
_counter = count(0)

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

async def _run():
    app = Application.builder().token(settings.BOT_TOKEN).build()
    await app.initialize()
    # Garante que não existe webhook configurado (evita conflito com polling remoto antigo)
    await app.bot.delete_webhook(drop_pending_updates=True)

    scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)
    scheduler.add_job(lambda: asyncio.create_task(tick(app)), "interval", hours=settings.INTERVAL_HOURS)
    scheduler.start()
    logger.info("Scheduler iniciado (prévia) — sem polling.")

    # Start do bot (necessário para inicializar o request), mas sem polling
    await app.start()
    # Mantém o processo vivo
    await asyncio.Event().wait()

def main():
    asyncio.run(_run())
