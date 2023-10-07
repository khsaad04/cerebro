import asyncio
import time
from random import choice, randint

from discord import Color, Embed, Member
from discord.ext import commands

from cogs import Plugin
from cogs.Games.views import ChessView
from core import Bot
from utils import Context


class Games(Plugin):
    """
    This is the Games cog, this cog contains games such as chess and math quiz
    """

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.hybrid_command(
        name="chess", description="Multiplayer chess game in discord"
    )
    async def chess_command(self, ctx: Context, member: Member) -> None:
        view = ChessView(ctx, member)
        fen = view.board.fen().split(" ")[0]
        embed = Embed(
            title="Chess",
            description=f"{view.white} vs {view.black}",
        )
        embed.set_image(url=f"https://chessimageapi.khsaad1.repl.co/board?fen={fen}")

        await ctx.send(f"{view.player.mention}'s turn", embed=embed, view=view)

    @commands.hybrid_command(name="math", description="Solve 5 math problems asap")
    async def math_command(self, ctx: Context) -> None:
        def gen_math():
            operator = str(choice(["+", "-", "*"]))
            if operator == "*":
                a = randint(1, 9)
                b = randint(1, 9)
            else:
                a = randint(1, 99)
                b = randint(1, 99)
            prob = f"{a}{operator}{b}"
            ans = {"+": a + b, "-": a - b, "*": a * b}[operator]
            return prob, ans

        embed = Embed(description="")
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        msg = await ctx.send(embed=embed)
        start_time = time.time()
        point = 0
        while point < 5:
            prob, ans = gen_math()
            embed.description = f"{str(prob)}\nCorrect answers: {point}/5"
            await msg.edit(embed=embed)

            def check(message):
                return (
                    message.author.id == ctx.author.id
                    and message.channel.id == ctx.channel.id
                )

            try:
                response = await self.bot.wait_for("message", check=check, timeout=30.0)
            except asyncio.TimeoutError:
                embed.description = "Timeout"
                await msg.edit(embed=embed)
                return

            if response.content == str(ans):
                point += 1
                embed.color = Color.green()
            elif response.content == "420":
                embed.description = "quit"
                await msg.edit(embed=embed)
                return
            else:
                embed.color = Color.red()

            await msg.edit(embed=embed)

        end_time = time.time()
        time_diff = round(end_time - start_time, 5)
        embed.description = f"5/5 | took {str(time_diff)}s"
        await msg.edit(embed=embed)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Games(bot))
