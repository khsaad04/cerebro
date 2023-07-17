from __future__ import annotations

from typing import Any, Optional

from discord import Color
from discord.ext.commands import Context as DefaultContext

from .embeds import Embed

__all__ = ("Context",)


class Context(DefaultContext):
    async def success(
        self,
        content: Optional[str] = None,
        embed: Optional[Embed] = None,
        *args: Any,
        **kwargs: Any,
    ):
        if embed is None:
            embed = Embed(title=self.command.qualified_name, description=content)
        return await super().send(embed=embed, **kwargs)

    async def error(
        self,
        content: Optional[str] = None,
        embed: Optional[Embed] = None,
        *args: Any,
        **kwargs: Any,
    ):
        if embed is None:
            embed = Embed(
                title=self.command.qualified_name,
                description=content,
                color=Color.red(),
            )
        return await super().send(embed=embed, **kwargs)
