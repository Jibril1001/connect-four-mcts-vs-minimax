import time
from typing import Optional

from engine import ConnectFour, Player
from agents.mcts import MCTSAgent
from agents.minimax import MinimaxAgent
from visualizer import Visualizer


class Arena:
    def __init__(self):
        self.game = ConnectFour()
        self.mcts = MCTSAgent(Player.RED, iterations=500)
        self.minimax = MinimaxAgent(Player.YELLOW, depth=4)
        self.vis = Visualizer()

        self.mcts_wins = 0
        self.minimax_wins = 0
        self.draws = 0

    def run_match(self, verbose: bool = True) -> Optional[Player]:
        self.game = ConnectFour()

        while not self.game.game_over:
            if verbose:
                self.vis.clear()
                self.vis.render(self.game)
                time.sleep(0.3)

            if self.game.current_player == Player.RED:
                col = self.mcts.get_move(self.game)
            else:
                col = self.minimax.get_move(self.game)

            self.game.play_turn(col)

        if self.game.winner == Player.RED:
            self.mcts_wins += 1
        elif self.game.winner == Player.YELLOW:
            self.minimax_wins += 1
        else:
            self.draws += 1

        if verbose:
            self.vis.clear()
            self.vis.render(self.game)

        return self.game.winner

    def run_tournament(self, matches: int = 10):
        print(f"\n🏆 TOURNAMENT: {matches} MATCHES 🏆\n")

        for i in range(matches):
            print(f"Match {i+1}/{matches}... ", end="", flush=True)
            winner = self.run_match(verbose=False)
            if winner == Player.RED:
                print("🔴 MCTS wins!")
            elif winner == Player.YELLOW:
                print("🟡 Minimax wins!")
            else:
                print("🤝 Draw!")

        print("\n" + "=" * 50)
        print("FINAL STATISTICS")
        print("=" * 50)
        print(f"MCTS (🔴):     {self.mcts_wins}/{matches} ({self.mcts_wins/matches*100:.1f}%)")
        print(f"Minimax (🟡):  {self.minimax_wins}/{matches} ({self.minimax_wins/matches*100:.1f}%)")
        print(f"Draws:         {self.draws}/{matches} ({self.draws/matches*100:.1f}%)")

        print("\n📊 ANALYSIS:")
        if self.mcts_wins > self.minimax_wins:
            print("  → MCTS performed better! Statistical simulation")
            print("    beats heuristic evaluation at this depth.")
        elif self.minimax_wins > self.mcts_wins:
            print("  → Minimax performed better! Perfect-play assumption")
            print("    works well for Connect Four.")
        else:
            print("  → Close match! Both algorithms show similar strength.")
