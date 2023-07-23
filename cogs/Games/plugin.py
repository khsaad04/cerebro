from discord import Embed, Member
from discord.ext import commands

from cogs import Plugin
from cogs.Games.views import ChessView
from core import Bot
from utils import Context


class Games(Plugin):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @commands.hybrid_command(name="chess")
    async def chess_command(self, ctx: Context, member: Member):
        view = ChessView(ctx, member)
        fen = view.board.fen().split(" ")[0]
        embed = Embed(
            title=f"{view.white} vs {view.black}",
            description=f"{view.player.mention} 's turn",
        )
        embed.set_image(url=f"https://chessimageapi.khsaad1.repl.co/board?fen={fen}")

        await ctx.send(embed=embed, view=view)


async def setup(bot: Bot):
    await bot.add_cog(Games(bot))
