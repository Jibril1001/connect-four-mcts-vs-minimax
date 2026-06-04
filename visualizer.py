import os
import sys

from engine import ConnectFour, Player

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


class Visualizer:
    def __init__(self):
        self.symbols = {Player.EMPTY: '.', Player.RED: '\U0001f534', Player.YELLOW: '\U0001f7e1'}

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _emoji(self, player: Player) -> str:
        return {Player.RED: '\U0001f534', Player.YELLOW: '\U0001f7e1'}.get(player, '')

    def render(self, state: ConnectFour):
        print("\n 0  1  2  3  4  5  6")
        print(" " + "-" * 25)
        for row in range(state.rows):
            line = ""
            for col in range(state.cols):
                piece = Player(state.board[row][col])
                line += f" {self.symbols[piece]} "
            print(line)
            print()

        if state.game_over:
            if state.winner:
                emoji = self._emoji(state.winner)
                name = "MCTS" if state.winner == Player.RED else "Minimax"
                print(f"\n{emoji} {name} WINS! {emoji}")
            else:
                print("\nDRAW!")
        else:
            emoji = self._emoji(state.current_player)
            name = "MCTS" if state.current_player == Player.RED else "Minimax"
            print(f"{emoji} {name}'s turn")
