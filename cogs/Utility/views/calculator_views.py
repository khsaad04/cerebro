from typing import Any

from discord import ButtonStyle, Embed, Interaction
from discord.ui import Button, View

from utils import Context

__all__ = ("CalculatorView",)


class CalculatorView(View):
    def __init__(self, ctx: Context):
        self.equation = ""
        self.display = ""
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

    async def interaction_check(self, interaction: Interaction):
        if interaction.user != self.ctx.author:
            interaction.response.send_message(
                "Let bro do his thing, you can use your own calculator", ephemeral=True
            )
            return False
        else:
            return True


class CalculatorButton(Button):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: Interaction):
        match self.label:
            case "C":
                self.view.equation = self.view.equation[:-1]
                self.view.display = self.view.display[:-1]

            case "=":
                self.view.display = eval(self.view.equation)
                self.view.equation = ""

            case "÷":
                self.view.equation = f"{self.view.equation}/"
                self.view.display = f"{self.view.display}{self.label}"

            case "×":
                self.view.equation = f"{self.view.equation}*"
                self.view.display = f"{self.view.display}{self.label}"

            case "%":
                self.view.equation = f"{self.view.equation}*0.01"
                self.view.display = f"{self.view.display}{self.label}"

            case _:
                self.view.equation = f"{self.view.equation}{self.label}"
                self.view.display = f"{self.view.display}{self.label}"

        embed = Embed(
            description=f"```                            \n{self.view.display}\n ```"
        )
        await interaction.response.edit_message(embed=embed)
        if not isinstance(self.view.display, str):
            self.view.display = ""
