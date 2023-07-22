from __future__ import annotations

from chess import Board
from discord.ui import View

__all__ = ("ChessView",)


class ChessView(View):
    def __init__(self):
        super().__init__()
        self.board = Board()

    async def get_board(self):
        return self.board
