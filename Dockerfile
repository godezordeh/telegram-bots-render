FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Ex.: BOT_ENTRY=bots.bot_previa:main  |  bots.bot_vip:main  |  bots.bot_pagamento:main
ENV BOT_ENTRY=bots.bot_previa:main

CMD ["python", "-c", "import importlib,os; m,f=os.environ['BOT_ENTRY'].split(':'); importlib.import_module(m).__dict__[f]()"]
