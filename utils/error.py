from __future__ import annotations

import sys
import traceback
from typing import Any

from discord import Embed
from discord.ext.commands import (
    BadArgument,
    ChannelNotFound,
    Cog,
    CommandError,
    CommandNotFound,
    MemberNotFound,
    MissingPermissions,
    MissingRequiredArgument,
)

from core import Bot
from utils import Context


class ErrorEmbed(Embed):
    def __init__(self, description: str, *args: Any, **kwargs: Any):
        super().__init__(description=description, *args, **kwargs)
        self.color = 0xFF0000
        self.title = "An error occurred"


class CommandErrorHandler(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if hasattr(ctx.command, "on_error"):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (CommandNotFound,)

        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, BadArgument):
            embed = ErrorEmbed(
                "Something went wrong, make sure you have passed the arguments correctly."
            )
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}{ctx.command.name} {ctx.command.signature}",
            )
            embed.set_footer(text="<> is required and [] is optional")

            await ctx.send(embed=embed)

        elif isinstance(error, MissingRequiredArgument):
            embed = ErrorEmbed("You are missing required arguments")
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}{ctx.command.name} {ctx.command.signature}",
            )
            embed.set_footer(text="<> is required and [] is optional")

            await ctx.send(embed=embed)

        elif isinstance(error, MemberNotFound):
            embed = ErrorEmbed(
                "Couldn't find the user. You can mention a member, write their username or give their user ID. Make sure you put the information correctly",
            )

            await ctx.send(embed=embed)

        elif isinstance(error, ChannelNotFound):
            embed = ErrorEmbed(
                "Couldn't find the channel.",
            )

            await ctx.send(embed=embed)

        elif isinstance(error, MissingPermissions):
            embed = ErrorEmbed(
                "You don't have all the required perms to use that command :)",
            )
            embed.add_field(
                name="Missing permissions",
                value="\n".join(error.missing_permissions),
            )
            await ctx.send(embed=embed)

        else:
            print(
                "Ignoring exception in command {}:".format(ctx.command), file=sys.stderr
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )


async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))
