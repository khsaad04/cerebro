from chess import Board
from discord import ButtonStyle, Embed, Interaction, TextStyle
from discord.ui import Button, Modal, TextInput, View, button

from utils import Context

__all__ = ("ChessView",)


class ChessView(View):
    def __init__(self, ctx: Context):
        super().__init__()
        self.board = Board()
        self.player = False
        self.ctx: Context = ctx

    @button(label="Move", style=ButtonStyle.green)
    async def move_button(self, interaction: Interaction, button: Button):
        legal_moves = [str(move) for move in list(self.board.legal_moves)]
        modal = ChessModal(title="Make your move")
        modal.add_item(TextInput(label="Your move", placeholder="example: e2e4"))
        modal.add_item(
            TextInput(
                label="Available moves",
                style=TextStyle.long,
                default=", ".join(legal_moves),
            ),
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        move = str(modal.children[0])
        try:
            self.board.push_uci(move)
        except Exception:
            await self.ctx.error("Invalid move")
        else:
            fen = self.board.fen().split(" ")[0]
            embed = Embed(title="Chess", description="White vs Nigga")
            embed.set_image(
                url=f"https://chessimageapi.khsaad1.repl.co/board?fen={fen}"
            )
            await interaction.message.edit(embed=embed, view=self)


class ChessModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
