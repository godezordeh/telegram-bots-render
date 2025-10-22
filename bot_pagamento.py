import asyncio, os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import settings
from utils import setup_logger

logger = setup_logger("bot_pagamento")

app = FastAPI()

# --- Telegram commands ---
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = settings.CHECKOUT_URL_TMPL.format(user_id=user.id)
    await update.message.reply_text("💳 Assine o VIP para liberar o conteúdo completo:\n" + link)

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        invite = await context.bot.create_chat_invite_link(settings.VIP_GROUP_ID, creates_join_request=False, name=f"VIP-{user.id}")
        await update.message.reply_text(f"✅ Seu acesso VIP: {invite.invite_link}")
    except Exception:
        logger.exception("Erro ao gerar convite VIP")
        await update.message.reply_text("Ainda não localizei sua assinatura. Se você já pagou, aguarde a confirmação do gateway ou me envie o comprovante.")

# --- FastAPI health ---
@app.get("/health")
def health():
    return {"ok": True}

# --- Webhook do gateway ---
class GatewayEvent(BaseModel):
    event: str
    data: dict

@app.post("/gateway/webhook")
async def gateway_webhook(request: Request, payload: GatewayEvent):
    secret = request.headers.get("X-Webhook-Secret")
    if secret != settings.GATEWAY_WEBHOOK_SECRET:
        raise HTTPException(401, "Invalid signature")

    if payload.event == "payment.succeeded":
        user_id = payload.data.get("user_id")
        if not user_id:
            raise HTTPException(400, "user_id missing")

        try:
            bot = tg_app.bot
            invite = await bot.create_chat_invite_link(settings.VIP_GROUP_ID, creates_join_request=False, name=f"VIP-{user_id}")
            msg = "🎉 Pagamento aprovado! Aqui está seu acesso VIP:\n" + invite.invite_link
            await bot.send_message(chat_id=int(user_id), text=msg)
            logger.info(f"Convite VIP enviado a {user_id}")
        except Exception:
            logger.exception("Falha ao enviar convite VIP")
            raise HTTPException(500, "Failed to deliver invite")

    return {"ok": True}

# --- Inicialização combinada PTB + FastAPI ---
tg_app: Application | None = None

def main():
    global tg_app

    tg_app = Application.builder().token(settings.BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", cmd_start))
    tg_app.add_handler(CommandHandler("status", cmd_status))

    async def run_all():
        await tg_app.initialize()
        await tg_app.start()
        logger.info("Bot de pagamento iniciado (polling).")
        await asyncio.Event().wait()

    import uvicorn
    loop = asyncio.get_event_loop()
    loop.create_task(run_all())
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
