from __future__ import annotations

from typing import Union

from discord import Interaction
from discord.ext import commands

from cogs import Plugin
from core import Bot

from .view import *


class Utility(Plugin):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.hybrid_command(name="ping", description="Shows the latency of the bot.")
    async def ping_command(self, ctx: Union[commands.Context, Interaction]):
        await self.bot.success(f"{self.bot.latency*1000:.2f} ms", ctx)

    @commands.hybrid_command(name="embed", description="Embed builder")
    async def embed_constructor_command(
        self, ctx: Union[commands.Context, Interaction]
    ):
        embed = Template.get_default_embed()
        view = EmbedBuilderSelect(embed=embed, ctx=ctx)
        await ctx.send(embed=embed, view=view)


async def setup(bot: Bot):
    await bot.add_cog(Utility(bot))
