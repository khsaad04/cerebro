from __future__ import annotations

from cogs import Plugin
from core import Bot


class Utility(Plugin):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot


async def setup(bot: Bot):
    await bot.add_cog(Utility(bot))
