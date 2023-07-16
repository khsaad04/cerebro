import os
from logging import getLogger

import discord
from discord import Intents
from discord.ext import commands

__all__ = ("Bot",)

log = getLogger("Bot")


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or(">"),
            intents=Intents.all(),
            case_insensitive=True,
        )

    async def on_connect(self):
        log.info(f"Connected to discord as {self.user}(ID:{self.user.id})")

    async def on_disconnect(self):
        log.info("Bot disconnected")

    async def on_resumed(self):
        log.info("Bot resumed")

    async def on_ready(self):
        log.info("Bot ready")

    async def setup_hook(self):
        log.info("Running setup...")
        for file in os.listdir("./cogs"):
            if not file.startswith("_"):
                await self.load_extension(f"cogs.{file}.plugin")
        synced_commands = await self.tree.sync()
        log.info(f"Synced {len(synced_commands)} commands")
        log.info("Setup complete.")
