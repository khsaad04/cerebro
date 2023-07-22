from __future__ import annotations

from typing import Any

from discord import ButtonStyle, Embed, Interaction
from discord.ui import Button, View

from utils import Context

__all__ = ("Calculator",)


class Calculator:
    def __init__(self, ctx: Context):
        self.equation = ""
        self.display = ""
        self.view = CalculatorView(ctx)

    def get_view(self):
        return self.view


class CalculatorView(View):
    def __init__(self, ctx: Context):
        super().__init__()
        self.ctx: Context = ctx

        button_row = float(0)

        for buttons in "()%C789÷456×123-0.=+":
            if buttons in "()%÷×-+":
                style = ButtonStyle.green
            elif buttons == "=":
                style = ButtonStyle.primary
            elif buttons == "C":
                style = ButtonStyle.danger
            else:
                style = ButtonStyle.secondary
            self.add_item(
                CalculatorButton(label=buttons, row=int(button_row), style=style)
            )
            button_row += 0.25

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user != self.ctx.author:
            interaction.response.send_message(
                "Let bro do his thing, you can use your own calculator", ephemeral=True
            )
            return False
        return True


class CalculatorButton(Button):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    async def callback(self, interaction: Interaction):
        match self.label:
            case "C":
                view.display = view.display[:-1]
                view.equation = view.display[:-1]
            case "=":
                view.display = eval(view.equation)
                view.equation = ""
            case "÷":
                view.display += self.label
                view.equation += "/"
            case "×":
                view.display += self.label
                view.equation += "*"
            case "%":
                view.display += self.label
                view.equation += "*0.01"
            case _:
                view.display += self.label
                view.equation += self.label
        embed = Embed(
            description=f"```                            \n{view.display}\n ```"
        )
        await interaction.response.edit_message(embed=embed)
        if not isinstance(view.display, str):
            view.display = ""
