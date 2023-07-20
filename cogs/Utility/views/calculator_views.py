from __future__ import annotations

from discord import Interaction
from discord.ui import View

from utils import Context

__all__ = ("CalculatorView",)


class CalculatorView(View):
    def __init__(self, equation: str, display: str, ctx: Context):
        super().__init__()
        self.equation: str = equation
        self.display: str = display
        self.ctx: Context = ctx

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user != self.ctx.author:
            interaction.response.send_message(
                "Let bro do his thing, you can use your own calculator", ephemeral=True
            )
            return False
        return True
