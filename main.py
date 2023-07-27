import asyncio
import os
from threading import Thread

from discord.utils import setup_logging
from flask import Flask

from core import Bot

token = os.environ.get("TOKEN")
app = Flask("")


@app.route("/")
def main():
    return "Your Bot Is Ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


async def main():
    setup_logging()
    keep_alive()
    async with Bot() as bot:
        await bot.start(token=token, reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())
