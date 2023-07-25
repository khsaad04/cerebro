from random import randint

from discord.ui import Button

__all__ = ("RespectButton",)


class RespectButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def callback(self, interaction):
        num = randint(1, 1000)
        if num == 69:
            await interaction.messsge.edit(content="Respect++", view=None)
        else:
            await interaction.message.edit(content="Fuck you", view=None)
