import asyncio
import os

from discord.utils import setup_logging

from core import Bot

token = os.environ.get("DISCORD_TOKEN")

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
    async with Bot() as bot:
        await bot.start(token=token, reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())
