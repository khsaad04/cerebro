from __future__ import annotations

from discord import ButtonStyle, Embed
from discord.ext import commands
from discord.ui import Button

from cogs import Plugin
from cogs.utility.views import CalculatorView, EmbedBuilderSelect, Template
from core import Bot
from utils import Context


class Utility(Plugin):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.hybrid_command(name="ping", description="Shows the latency of the bot.")
    async def ping_command(self, ctx: Context):
        await ctx.send(f"{self.bot.latency*1000:.2f} ms")

    @commands.hybrid_command(name="embed", description="Embed builder")
    async def embed_constructor_command(self, ctx: Context):
        embed = Template.get_default_embed()
        view = EmbedBuilderSelect(embed=embed, ctx=ctx)
        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(name="calc")
    async def calculator_command(self, ctx: Context):
        view = CalculatorView("", "")

        class CalculatorButton(Button):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

            async def callback(self, interaction):
                if self.label == "C":
                    view.display = view.display[:-1]
                    view.equation = view.display[:-1]
                elif self.label == "=":
                    view.display = eval(view.equation)
                    view.equation = ""
                elif self.label == "÷":
                    view.display += self.label
                    view.equation += "/"
                elif self.label == "×":
                    view.display += self.label
                    view.equation += "*"
                elif self.label == "%":
                    view.display += self.label
                    view.equation += "*0.01"
                else:
                    view.display += self.label
                    view.equation += self.label
                embed = Embed(
                    description=f"```                            \n{view.display}\n ```"
                )
                await interaction.response.edit_message(embed=embed)
                if not isinstance(view.display, str):
                    view.display = ""

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
            view.add_item(
                CalculatorButton(label=buttons, row=int(button_row), style=style)
            )
            button_row += 0.25

        embed = Embed(description="```                            \n \n ```")
        await ctx.send(embed=embed, view=view)


async def setup(bot: Bot):
    await bot.add_cog(Utility(bot))
