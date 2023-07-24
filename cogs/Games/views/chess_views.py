from chess import Board
from discord import ButtonStyle, Embed, Interaction, Member, TextStyle
from discord.ui import Button, Modal, TextInput, View, button

from utils import Context

__all__ = ("ChessView",)


class ChessView(View):
    def __init__(self, ctx: Context, member: Member):
        super().__init__()

        self.white = ctx.author
        self.black = member

        self.board = Board()
        self.player = self.white
        self.flip = False
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
                required=False,
            ),
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        move = str(modal.children[0])
        before = move[:-2]
        after = move[2:]
        try:
            self.board.push_uci(move)
            if self.board.is_checkmate():
                fen = self.board.fen().split(" ")[0]
                embed = Embed(
                    title=f"{self.white} vs {self.black}",
                    description=f"{self.white if self.player is self.black else self.black} won by checkmate!",
                )
                embed.set_image(
                    url=f"https://chessimageapi.khsaad1.repl.co/board?fen={fen}&flip={self.flip}&before={before}&after={after}"
                )
                return await interaction.message.edit(embed=embed, view=None)
        except Exception:
            await self.ctx.error("Invalid move")
        else:
            self.flip = True if self.flip is False else False
            self.player = self.black if self.player is self.white else self.white
            fen = self.board.fen().split(" ")[0]
            embed = Embed(
                title=f"{self.white} vs {self.black}",
                description=f"{self.player.mention} 's turn",
            )
            embed.set_image(
                url=f"https://chessimageapi.khsaad1.repl.co/board?fen={fen}&flip={self.flip}&before={before}&after={after}"
            )
            await interaction.message.edit(embed=embed, view=self)

    @button(label="Resign", style=ButtonStyle.danger)
    async def resign_button(self, interaction: Interaction, button: Button):
        self.player = self.black if self.player is self.white else self.white
        await interaction.message.edit(
            content=f"{self.player.mention} won by resignation", view=None
        )

    async def interaction_check(self, interaction: Interaction):
        if interaction.user != self.player:
            await interaction.response.send_message(
                "It's not your turn", ephemeral=True
            )
            return False
        return True


class ChessModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
