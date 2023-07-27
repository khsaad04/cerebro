import asyncio
import os

from discord.utils import setup_logging

from core import Bot

token = os.environ.get("TOKEN")


async def main():
    setup_logging()
    async with Bot() as bot:
        await bot.start(token=token, reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())
