from __future__ import annotations

from discord import Interaction
from discord.ui import View

__all__ = ("CalculatorView",)


class CalculatorView(View):
    def __init__(self, equation: str, display: str):
        super().__init__()
        self.equation = equation
        self.display = display

    async def interaction_check(self, interaction: Interaction):
        if interaction.user != self.ctx.author:
            interaction.response.send_message(
                "Let bro do his thing, you can use your own calculator", ephemeral=True
            )
            return False
        else:
            return True
