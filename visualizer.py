import os

from engine import ConnectFour, Player


class Visualizer:
    def __init__(self):
        self.symbols = {Player.EMPTY: '·', Player.RED: '🔴', Player.YELLOW: '🟡'}

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self, state: ConnectFour):
        print("\n  0   1   2   3   4   5   6")
        print(" ─────────────────────────")
        for row in range(state.rows):
            line = ""
            for col in range(state.cols):
                piece = Player(state.board[row][col])
                line += f" {self.symbols[piece]} "
            print(line)
            print()

        if state.game_over:
            if state.winner:
                winner = "🔴 MCTS" if state.winner == Player.RED else "🟡 Minimax"
                print(f"\n🏆 {winner} WINS! 🏆")
            else:
                print("\n🤝 DRAW! 🤝")
        else:
            current = "🔴 MCTS" if state.current_player == Player.RED else "🟡 Minimax"
            print(f"\n➡ {current}'s turn")
