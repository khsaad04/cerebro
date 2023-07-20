from __future__ import annotations

from discord import Color, Embed, Member, app_commands
from discord.ext import commands

from cogs import Plugin
from core import Bot
from utils import Context


class Moderation(Plugin):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    # kick_command
    @commands.hybrid_command(name="kick", description="Kick a member from the server")
    @commands.has_permissions(kick_members=True)
    @app_commands.describe(
        member="The person you want to kick", reason="The reason you want to kick them"
    )
    async def kick_command(
        self,
        ctx: Context,
        member: Member,
        *,
        reason: str = "No reason provided",
    ):
        member = member
        embed = Embed(
            title="User kicked",
            description=f"{member} has been kicked. for: {reason}",
            color=Color.green(),
        )
        embed.set_footer(
            icon_url=ctx.author.avatar, text=f"kicked by {ctx.author.name}"
        )
        embed.set_thumbnail(url=member.avatar)
        try:
            await member.send(f"You have been kicked from PUBGM HANGOUT for: {reason}")
        except Exception:
            await ctx.error("Couldn't dm them")

        finally:
            try:
                await member.kick(reason=reason)
                await ctx.send(embed=embed)
            except Exception:
                await ctx.error("Couldn't kick them")


async def setup(bot: Bot):
    await bot.add_cog(Moderation(bot))
