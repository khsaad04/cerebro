import asyncio
import os

from discord.utils import setup_logging

from core import Bot
from keep_alive import keep_alive

token = os.environ.get("TOKEN")


async def main():
    setup_logging()
    keep_alive()
    async with Bot() as bot:
        await bot.start(token=token, reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())
