from typing import Any, Optional

from discord import Color, Embed
from discord.ext.commands import Context as DefaultContext

__all__ = ("Context",)


class Context(DefaultContext):
    async def send(
        self,
        content: Optional[str] = None,
        *args: Any,
        embed: Optional[Embed] = None,
        create_embed: Optional[bool] = False,
        **kwargs: Any,
    ):
        if create_embed and embed is None:
            embed = Embed(
                title=self.command.qualified_name, description=content, color=0xC246B3
            )
            embed.set_footer(
                icon_url=self.author.avatar, text=f"invoked by {self.author}"
            )
            content = None

        return await super().send(content, embed=embed, **kwargs)

    async def error(
        self,
        content: Optional[str] = None,
        *args: Any,
        embed: Optional[Embed] = None,
        **kwargs: Any,
    ):
        if create_embed and embed:
            embed = Embed(
                title="An error occurred", description=content, color=Color.red()
            )
            embed.set_footer(
                icon_url=self.author.avatar, text=f"invoked by {self.author}"
            )
            content = None

        return await super().send(content, embed=embed, ephemeral=True, **kwargs)
