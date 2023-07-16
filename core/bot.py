from __future__ import annotations

import os
from logging import getLogger
from typing import Any, Optional, Union

from discord import Intents, Interaction
from discord.ext import commands

from utils import Embed

__all__ = ("Bot",)

log = getLogger("Bot")


class Bot(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(
            command_prefix=commands.when_mentioned_or(">"),
            intents=Intents.all(),
            case_insensitive=True,
        )

    async def on_connect(self):
        log.info(f"Connected to discord as {self.user}(ID:{self.user.id})")

    async def on_disconnect(self):
        log.info("Bot disconnected")

    async def on_resumed(self):
        log.info("Bot resumed")

    async def on_ready(self):
        log.info("Bot ready")

    async def setup_hook(self):
        log.info("Running setup...")
        for file in os.listdir("./cogs"):
            if not file.startswith("_"):
                await self.load_extension(f"cogs.{file}.plugin")
        synced_commands = await self.tree.sync()
        log.info(f"Synced {len(synced_commands)} commands")
        log.info("Setup complete.")

    async def success(
        self,
        msg: str,
        ctx: Union[commands.Context, Interaction],
        *,
        ephemeral: Optional[bool] = False,
        embed: Optional[bool] = True,
        embed_title: Optional[str] = None,
    ):
        if embed_title is None:
            embed_title = ctx.command.qualified_name
        em = Embed(title=embed_title, description=msg)
        if isinstance(ctx, Interaction):
            if embed:
                if ctx.response.is_done():
                    return await ctx.followup.send(embed=em, ephemeral=ephemeral)
                return await ctx.response.send_message(embed=em, ephemeral=ephemeral)
            if ctx.response.is_done():
                return await ctx.followup.send(content=msg, ephemeral=ephemeral)
            return await ctx.response.send_message(msg, ephemeral=ephemeral)

        else:
            if embed:
                return await ctx.send(embed=em)
            return await ctx.send(msg)

    async def error(
        self,
        msg: str,
        ctx: Union[commands.Context, Interaction],
        *,
        ephemeral: Optional[bool] = True,
        embed: Optional[bool] = True,
        embed_title: Optional[str] = None,
    ):
        if embed_title is None:
            embed_title = ctx.command.qualified_name
        em = Embed(title=embed_title, description=msg)
        if isinstance(ctx, Interaction):
            if embed:
                if ctx.response.is_done():
                    return await ctx.followup.send(embed=em, ephemeral=ephemeral)
                return await ctx.response.send_message(embed=em, ephemeral=ephemeral)
            if ctx.response.is_done():
                return await ctx.followup.send(content=msg, ephemeral=ephemeral)
            return await ctx.response.send_message(msg, ephemeral=ephemeral)

        else:
            if embed:
                return await ctx.send(embed=em)
            return await ctx.send(msg)
