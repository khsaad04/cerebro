from discord import Embed
from discord.ext import commands

from cogs import Plugin
from cogs.Games.views import ChessView
from core import Bot
from utils import Context


class Games(Plugin):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @commands.hybrid_command(name="chess")
    async def chess_command(self, ctx: Context):
        view = ChessView(ctx)
        fen = view.board.fen().split(" ")[0]
        embed = Embed(title="Chess", description="White vs Nigga")
        embed.set_image(url=f"https://chessimageapi.khsaad1.repl.co/board?fen={fen}")

        await ctx.send(embed=embed, view=view)


async def setup(bot: Bot):
    await bot.add_cog(Games(bot))
