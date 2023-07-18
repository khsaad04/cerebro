from __future__ import annotations

from discord.ext import commands

from cogs import Plugin
from cogs.utility.views import *
from core import Bot
from utils import Context


class Utility(Plugin):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.hybrid_command(name="ping", description="Shows the latency of the bot.")
    async def ping_command(self, ctx: Context):
        await ctx.send(f"{self.bot.latency*1000:.2f} ms")

    @commands.hybrid_command(name="embed", description="Embed builder")
    async def embed_constructor_command(self, ctx: Context):
        embed = Template.get_default_embed()
        view = EmbedBuilderSelect(embed=embed, ctx=ctx)
        await ctx.send(embed=embed, view=view)


async def setup(bot: Bot):
    await bot.add_cog(Utility(bot))
