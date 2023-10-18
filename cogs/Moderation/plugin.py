from datetime import timedelta
from typing import Optional, Union

import discord
from discord import Member, User, app_commands
from discord.ext import commands
from humanfriendly import InvalidTimespan, parse_timespan

from cogs import Plugin
from core import Bot
from utils import Context


class Moderation(Plugin):
    """
    This is the Moderation cog. This cog includes most commands
    that'll assist the moderators to maintain their servers.
    """

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    def can_moderate(
        self,
        ctx: Context,
        member: Member,
    ) -> Union[str, bool]:
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

    # import stuff
    @commands.Cog.listener(name = "on_member_join")
    async def _ban_fools(self, member: discord.Member):
        blacklist = [872642439159087106, 744478249719169074]
        if member.id in blacklist:
            await member.ban(reason = "You are not worthy.")

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
    ) -> None:
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

        await ctx.send(f"{member} has been kicked for {reason}", create_embed=True)

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
    ) -> None:
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

        await ctx.send(f"{member} has been banned for {reason}", create_embed=True)

    @commands.hybrid_command(
        name="unban", description="Unban a person who is currently banned"
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @app_commands.describe(
        user="The user you want to unban", reason="The reason for it"
    )
    async def unban_command(
        self,
        ctx: Context,
        user: User,
        *,
        reason: Optional[str] = "no reason whatsoever",
    ) -> None:
        try:
            await ctx.guild.unban(user, reason=reason)
        except discord.NotFound:
            return await ctx.error(f"{user.mention} is not banned from this server.")
        else:
            await ctx.send(f"Unbanned {user.mention}", create_embed=True)

    # mute_command
    @commands.hybrid_command(name="mute", description="Mute/timeout a member")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @app_commands.describe(
        member="The person you want to mute",
        duration="The amount of time you wanna mute him for",
        reason="The reason for it",
    )
    async def mute_command(
        self,
        ctx: Context,
        member: Member,
        duration: Optional[str] = "1d",
        *,
        reason: Optional[str] = "no reason whatsoever",
    ) -> None:
        if check_made := self.can_moderate(ctx, member):
            return await ctx.error(check_made)

        try:
            real_duration = parse_timespan(duration)
        except InvalidTimespan:
            await ctx.error("Invalid duration")
        else:
            try:
                await member.timeout(
                    discord.utils.utcnow() + timedelta(seconds=real_duration),
                    reason=reason,
                )
            except Exception:
                await ctx.error("Something went wrong while tryig to mute that person!")
            else:
                await ctx.send(f"{member.mention} has been muted for {duration}", create_embed=True)

    @commands.hybrid_command(
        name="unmute", description="Unmute/remove timeout from a member"
    )
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @app_commands.describe(
        member="The person you want to mute",
        reason="The reason for it",
    )
    async def unmute_command(
        self,
        ctx: Context,
        member: Member,
        *,
        reason: Optional[str] = "no reason whatsoever",
    ) -> None:
        if check_made := self.can_moderate(ctx, member):
            return await ctx.error(check_made)

        if not member.is_timed_out:
            await ctx.error(f"{member.mention} is not timed out!")
        else:
            try:
                await member.timeout(None)
            except Exception:
                await ctx.error("Something went wrong!")
            else:
                await ctx.send(f"Successfully unmuted {member.mention}", create_embed=True)

    # slowmode_command
    @commands.hybrid_command(
        name="slowmode", description="Set a slowmode for the particular channel"
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @app_commands.describe(seconds="Slowmode time")
    async def slowmode_command(self, ctx: Context, seconds: int) -> None:
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
        except Exception:
            await ctx.error("Couldn't set a slowmode")
        else:
            await ctx.send(f"Slowmode is now {seconds}s", create_embed=True)

    # purge_command
    @commands.hybrid_command(
        name="purge",
        description="Purges the chat as per the given amount.",
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_channels=True)
    @app_commands.describe(amount="The number of messages to delete/purge")
    async def clear_command(self, ctx: Context, amount=1) -> None:
        try:
            await ctx.channel.purge(limit=amount + 1)
        except Exception:
            await ctx.error("Couldn't purge for some reason")
        else:
            await ctx.send(f"deleted {amount} message(s)", create_embed=True,delete_after=5.0)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Moderation(bot))
