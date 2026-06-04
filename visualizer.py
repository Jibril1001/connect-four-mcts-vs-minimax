import os
import sys

from engine import ConnectFour, Player

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


class Visualizer:
    def __init__(self):
        self.symbols = {Player.EMPTY: '\u3000', Player.RED: '\U0001f534', Player.YELLOW: '\U0001f7e1'}

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _emoji(self, player: Player) -> str:
        return {Player.RED: '\U0001f534', Player.YELLOW: '\U0001f7e1'}.get(player, '')

    def render(self, state: ConnectFour):
        print()
        for c in range(state.cols):
            print(f"  {c} ", end="")
        print()
        for c in range(state.cols):
            print(f" {'.' * 2} ", end="")
        print()
        for row in range(state.rows):
            for col in range(state.cols):
                piece = Player(state.board[row][col])
                symbol = self.symbols[piece]
                print(f" {symbol} ", end="")
            print()
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
