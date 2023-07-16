from __future__ import annotations

from typing import Any, Union

from discord import Color
from discord import Embed as DefaultEmbed

__all__ = ("Embed",)


class Embed(DefaultEmbed):
    def __init__(
        self,
        color: Union[int, Color] = Color(int("C246B3", 16)),
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(color=color, **kwargs)
