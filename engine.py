from enum import Enum
from typing import List


class Player(Enum):
    EMPTY = 0
    RED = 1
    YELLOW = 2


class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = Player.RED
        self.winner = None
        self.game_over = False

    def get_valid_moves(self) -> List[int]:
        return [c for c in range(self.cols) if self.board[0][c] == 0]

    def drop_row(self, col: int) -> int:
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                return row
        return -1

    def make_move(self, col: int, player: Player) -> bool:
        if col not in self.get_valid_moves():
            return False
        row = self.drop_row(col)
        self.board[row][col] = player.value
        return True

    def check_win(self, row: int, col: int, player: Player) -> bool:
        val = player.value
        for c in range(max(0, col - 3), min(self.cols - 4, col) + 1):
            if all(self.board[row][c + i] == val for i in range(4)):
                return True
        for r in range(max(0, row - 3), min(self.rows - 4, row) + 1):
            if all(self.board[r + i][col] == val for i in range(4)):
                return True
        for d in range(-3, 1):
            r, c = row + d, col + d
            if 0 <= r <= self.rows - 4 and 0 <= c <= self.cols - 4:
                if all(self.board[r + i][c + i] == val for i in range(4)):
                    return True
        for d in range(-3, 1):
            r, c = row - d, col + d
            if 3 <= r < self.rows and 0 <= c <= self.cols - 4:
                if all(self.board[r - i][c + i] == val for i in range(4)):
                    return True
        return False

    def play_turn(self, col: int) -> bool:
        if self.game_over:
            return False
        if not self.make_move(col, self.current_player):
            return False
        row = self.drop_row(col) + 1
        if self.check_win(row, col, self.current_player):
            self.winner = self.current_player
            self.game_over = True
        elif len(self.get_valid_moves()) == 0:
            self.game_over = True
        else:
            self.current_player = Player.YELLOW if self.current_player == Player.RED else Player.RED
        return True

    def clone(self):
        new = ConnectFour()
        new.board = [row[:] for row in self.board]
        new.current_player = self.current_player
        new.winner = self.winner
        new.game_over = self.game_over
        return new
