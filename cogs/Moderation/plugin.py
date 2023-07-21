from __future__ import annotations

from typing import Optional

import discord
from discord import Member, User, app_commands
from discord.ext import commands

from cogs import Plugin
from core import Bot
from utils import Context


class Moderation(Plugin):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    def can_moderate(
        self,
        ctx: Context,
        member: Member,
    ):
        if isinstance(member, User):
            return False

        if member == ctx.author:
            return f"You thought you could {ctx.command.qualified_name} yourself? Bruh"
        elif member == ctx.guild.owner:
            return f"You can't {ctx.command.qualified_name} the server owner."
        elif (
            ctx.author.top_role.position <= member.top_role.position
            and ctx.author != ctx.guild.owner
        ):
            return (
                f"You can't {ctx.command.qualified_name} this member. "
                "They have a higher or equal role than you."
            )
        elif ctx.guild.me.top_role.position <= member.top_role.position:
            return (
                f"I can't {ctx.command.qualified_name} this member. "
                "They have a higher or equal role than me."
            )

        return False

    # kick_command
    @commands.hybrid_command(name="kick", description="Kick a member from the server")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @app_commands.describe(
        member="The person you want to kick", reason="The reason you want to kick them"
    )
    async def kick_command(
        self,
        ctx: Context,
        member: Member,
        *,
        reason: Optional[str] = "no reason whatsoever",
    ):
        if check_made := self.can_moderate(ctx, member):
            return await ctx.error(check_made)

        try:
            await member.kick(reason=reason)
            try:
                await member.send(
                    f"You have been kicked from {ctx.guild.name} for {reason}"
                )
            except Exception:
                pass

        except Exception:
            await ctx.error("Couldn't kick them")
            return

        await ctx.send(f"{member} has been kicked for {reason}")

    # ban_command
    @commands.hybrid_command(name="ban", description="Ban a member from the server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @app_commands.describe(
        member="The person you want to ban", reason="The reason you want to ban them"
    )
    async def ban_command(
        self,
        ctx: Context,
        member: Member,
        *,
        reason: Optional[str] = "no reason whatsoever",
    ):
        if check_made := self.can_moderate(ctx, member):
            return await ctx.error(check_made)

        try:
            await member.ban(reason=reason)
            try:
                await member.send(
                    f"You have been banned from {ctx.guild.name} for {reason}"
                )
            except Exception:
                pass

        except Exception:
            await ctx.error("Couldn't ban them")
            return

        await ctx.send(f"{member} has been banned for {reason}")


async def setup(bot: Bot):
    await bot.add_cog(Moderation(bot))
