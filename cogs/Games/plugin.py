from discord import Embed, Interaction, SelectOption
from discord.ext import commands
from discord.ui import Select

from cogs import Plugin
from cogs.Games.views import ChessView
from core import Bot
from utils import Context


class Games(Plugin):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @commands.hybrid_command(name="chess")
    async def chess_command(self, ctx: Context):
        view = ChessView()
        board = await view.get_board()
        fen = board.fen()
        fen = fen.split(" ")[0]
        embed = Embed(title="Chess", description="White vs Nigga")
        embed.set_image(url=f"https://chessimageapi.khsaad1.repl.co/board?fen={fen}")

        class ChessSelect(Select):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            async def callback(self, interaction: Interaction):
                view.board.push_uci(self.values[0])
                embed = Embed(title="Chess", description="White vs Nigga")
                embed.set_image(
                    url=f"https://chessimageapi.khsaad1.repl.co/board?fen={fen}"
                )
                await interaction.message.edit(embed=embed, view=view)

        select = ChessSelect(
            placeholder="Make your move",
            options=[
                SelectOption(label=str(moves), value=str(moves))
                for moves in list(view.board.legal_moves)
            ],
            max_values=1,
        )

        view.add_item(select)

        await ctx.send(embed=embed, view=view)


async def setup(bot: Bot):
    await bot.add_cog(Games(bot))
