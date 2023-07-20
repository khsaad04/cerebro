from __future__ import annotations

import random

from discord import app_commands
from discord.ext import commands

from cogs import Plugin
from core import Bot
from utils import Context


class Fun(Plugin):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    # 8ball command
    @commands.hybrid_command(
        name="8ball",
        description="Ask any question for a random answer.",
    )
    @app_commands.describe(question="The question you want to ask")
    async def _8ball_command(self, ctx: Context, *, question: str):
        replies = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Dont count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]

        ans = f"{ctx.author.mention} asked: {question} \nAns: {random.choice(replies)}"

        await ctx.send(ans)


async def setup(bot: Bot):
    await bot.add_cog(Fun(bot))
