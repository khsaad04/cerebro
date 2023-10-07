from typing import Any

from discord import ButtonStyle, Embed, Interaction
from discord.ui import Button, View

from utils import Context

__all__ = ("CalculatorView",)


class CalculatorView(View):
    def __init__(self, ctx: Context) -> None:
        self.equation: str = ""
        self.display: str = ""
        self.ctx: Context = ctx
        super().__init__()

        for row, label in enumerate("()%C789÷456×123-0.=+"):
            if label in "()%÷×-+":
                style = ButtonStyle.green
            elif label == "=":
                style = ButtonStyle.primary
            elif label == "C":
                style = ButtonStyle.danger
            else:
                style = ButtonStyle.secondary

            self.add_item(CalculatorButton(label=label, row=row // 4, style=style))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "Let bro do his thing, you can use your own calculator", ephemeral=True
            )
            return False
        return True


class CalculatorButton(Button):
    async def callback(self, interaction: Interaction) -> None:
        view: CalculatorView = self.view
        label: str = self.label
        match label:
            case "C":
                view.equation = view.equation[:-1]
                view.display = view.display[:-1]

            case "=":
                view.display = eval(view.equation)
                view.equation = ""

            case "÷":
                view.equation = f"{view.equation}/"
                view.display = f"{view.display}{label}"

            case "×":
                view.equation = f"{view.equation}*"
                view.display = f"{view.display}{label}"

            case "%":
                view.equation = f"{view.equation}*0.01"
                view.display = f"{view.display}{label}"

            case _:
                view.equation = f"{view.equation}{label}"
                view.display = f"{view.display}{label}"

        embed = Embed(
            description=f"```                            \n{view.display}\n ```"
        )
        await interaction.response.edit_message(embed=embed)
        if not isinstance(view.display, str):
            view.display = ""
