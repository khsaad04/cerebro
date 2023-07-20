from __future__ import annotations

from typing import Any, Optional

from discord import Embed
from discord.ext.commands import Context as DefaultContext

__all__ = ("Context",)


class Context(DefaultContext):
    async def send(
        self,
        content: Optional[str] = None,
        *args: Any,
        embed: Optional[Embed] = None,
        **kwargs: Any,
    ):
        if embed is None:
            embed = Embed(
                title=self.command.qualified_name, description=content, color=0xC246B3
            )
            embed.set_footer(icon_url=self.author.avatar, text=f"{self.author}")
        return await super().send(embed=embed, **kwargs)

    async def error(
        self,
        content: Optional[str] = None,
        *args: Any,
        embed: Optional[Embed] = None,
        **kwargs: Any,
    ):
        if embed is None:
            embed = Embed(
                title=self.command.qualified_name, description=content, color=0xFF0000
            )
        return await super().send(embed=embed, **kwargs)
