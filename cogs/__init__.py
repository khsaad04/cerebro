from __future__ import annotations

from logging import getLogger

from discord.ext import commands

from core import Bot

__all__ = ("Plugin",)

log = getLogger(__name__)


class Plugin(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

    async def cog_load(self):
        log.info(f"Loaded {self.qualified_name} cog")

    async def cog_unload(self):
        log.info(f"Unloaded {self.qualified_name} cog")
