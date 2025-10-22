# Telegram Bots (Prévia, VIP, Pagamentos) para Render

## Serviços
- Worker: `bot-previa` (envia prévias a cada 6h)
- Worker: `bot-vip` (envia conteúdo VIP a cada 6h)
- Web: `bot-pagamento` (link de checkout + webhook do gateway + convite VIP)

## Variáveis de ambiente essenciais
### bot-previa
- `BOT_ENTRY=bots.bot_previa:main`
- `BOT_TOKEN=<token>`
- `GROUP_ID=<id grupo free>`
- `TIMEZONE=America/Sao_Paulo`
- `INTERVAL_HOURS=6`
- `MEDIA_DIR=media/previas` (opcional)
- `MEDIA_URLS_JSON=["https://..."]` (opcional)

### bot-vip
- `BOT_ENTRY=bots.bot_vip:main`
- `BOT_TOKEN=<token>`
- `GROUP_ID=<id grupo vip>`
- `TIMEZONE=America/Sao_Paulo`
- `INTERVAL_HOURS=6`
- `MEDIA_DIR=media/vip` (opcional)
- `MEDIA_URLS_JSON=["https://..."]` (opcional)

### bot-pagamento (web)
- `BOT_ENTRY=bots.bot_pagamento:main`
- `BOT_TOKEN=<token>`
- `VIP_GROUP_ID=<id grupo vip>`
- `CHECKOUT_URL_TMPL=https://...{user_id}&hash=...`
- `GATEWAY_WEBHOOK_SECRET=<secret>`
- `PUBLIC_BASE_URL=https://seu-servico.onrender.com` (opcional)
- `TIMEZONE=America/Sao_Paulo`

## Deploy
- Suba este diretório para um repositório e conecte no Render.
- O `render.yaml` cria 3 serviços (2 workers + 1 web).

