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
    @commands.bot_has_permissions(kick_members=True)
    @app_commands.default_permissions(kick_members=True)
    @app_commands.describe(
        member="The person you want to kick", reason="The reason you want to kick them"
    )
    async def kick_command(
        self,
        ctx: Context,
        member: Member,
        *,
        reason: str = "no reason whatsoever",
    ):
        if ctx.author == member:
            return await ctx.error("Imagine trying to kick yourself, what a retard")

        elif member == ctx.guild.owner:
            return await ctx.error(f"{member.mention} is the owner")

        elif ctx.me.top_role < member.top_role:
            return await ctx.error("I'm not able to kick them")

        elif (
            ctx.author.top_role < member.top_role
            and not ctx.author.guild_permissions.administrator
            and not ctx.author.guild.owner == ctx.author
        ):
            return await ctx.error("You can't kick them")

        description = f"{member} has been kicked for {reason}"

        try:
            await member.kick(reason=reason)
            try:
                await member.send(
                    f"You have been kicked from {ctx.guild.name} for {reason}"
                )
            except Exception:
                description = "".join([description, "\ncouldn't dm them"])
        except Exception:
            await ctx.error("Couldn't kick them")
        else:
            await ctx.send(description)

    # ban_command
    @commands.hybrid_command(name="ban", description="Ban a member from the server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @app_commands.default_permissions(ban_members=True)
    @app_commands.describe(
        member="The person you want to ban", reason="The reason you want to ban them"
    )
    async def ban_command(
        self,
        ctx: Context,
        member: Member,
        *,
        reason: str = "no reason whatsoever",
    ):
        if ctx.author == member:
            return await ctx.error("Imagine trying to ban yourself, what a retard")

        elif member == ctx.guild.owner:
            return await ctx.error(f"{member.mention} is the owner")

        elif ctx.me.top_role < member.top_role:
            return await ctx.error("I'm not able to ban them")

        elif (
            ctx.author.top_role < member.top_role
            and not ctx.author.guild_permissions.administrator
            and not ctx.author.guild.owner == ctx.author
        ):
            return await ctx.error("You can't ban them")

        description = f"{member} has been banned for {reason}"

        try:
            await member.ban(reason=reason)
            try:
                await member.send(
                    f"You have been banned from {ctx.guild.name} for {reason}"
                )
            except Exception:
                description = "".join([description, "\ncouldn't dm them"])
        except Exception:
            await ctx.error("Couldn't ban them")
        else:
            await ctx.send(description)


async def setup(bot: Bot):
    await bot.add_cog(Moderation(bot))
