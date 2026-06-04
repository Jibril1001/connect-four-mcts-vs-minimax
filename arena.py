import time
from typing import Optional

from engine import ConnectFour, Player
from agents.mcts import MCTSAgent
from agents.minimax import MinimaxAgent
from visualizer import Visualizer


class Arena:
    def __init__(self):
        self.game = ConnectFour()
        self.mcts = MCTSAgent(iterations=500)
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

    def live_fight(self):
        self.game = ConnectFour()
        print("\n" + "=" * 55)
        print("   LIVE ARENA: MCTS vs MINIMAX")
        print("=" * 55)
        print("   \U0001f534 MCTS     \U0001f7e1 Minimax")

        while not self.game.game_over:
            self.vis.clear()
            self.vis.render(self.game)

            if self.game.current_player == Player.RED:
                print("\n[MCTS] is analyzing the board...")
                print("   Simulating possible futures...")
                col = self.mcts.get_move(self.game)
                print(f"  -> MCTS drops piece in column {col}")
            else:
                print("\n[Minimax] is computing optimal play...")
                print("   Searching game tree with Alpha-Beta pruning...")
                col = self.minimax.get_move(self.game)
                print(f"  -> Minimax drops piece in column {col}")

            self.game.play_turn(col)
            time.sleep(1.2)

        self.vis.clear()
        self.vis.render(self.game)
        return self.game.winner

    def interactive_mode(self):
        print("\n" + "=" * 55)
        print("   INTERACTIVE MODE: Play against AI")
        print("=" * 55)
        print("1. Play against MCTS (statistical)")
        print("2. Play against Minimax (heuristic)")
        choice = input("Choose (1-2): ")

        ai = self.mcts if choice == '1' else self.minimax
        self.game = ConnectFour()
        human = Player.RED

        while not self.game.game_over:
            self.vis.clear()
            self.vis.render(self.game)

            if self.game.current_player == human:
                try:
                    col = int(input(f"\nYour move (0-6): "))
                    if col not in self.game.get_valid_moves():
                        print("Invalid! That column is full.")
                        continue
                except ValueError:
                    print("Enter a number 0-6!")
                    continue
            else:
                print("\nAI thinking...")
                time.sleep(0.8)
                col = ai.get_move(self.game)
                print(f"AI chooses column {col}")
                time.sleep(0.5)

            self.game.play_turn(col)

        self.vis.clear()
        self.vis.render(self.game)
        return self.game.winner

    def run_tournament(self, matches: int = 10):
        print(f"\n[TOURNAMENT] {matches} MATCHES\n")

        for i in range(matches):
            print(f"Match {i+1}/{matches}... ", end="", flush=True)
            winner = self.run_match(verbose=False)
            if winner == Player.RED:
                print("MCTS wins!")
            elif winner == Player.YELLOW:
                print("Minimax wins!")
            else:
                print("Draw!")

        print("\n" + "=" * 50)
        print("FINAL STATISTICS")
        print("=" * 50)
        print(f"MCTS:     {self.mcts_wins}/{matches} ({self.mcts_wins/matches*100:.1f}%)")
        print(f"Minimax:  {self.minimax_wins}/{matches} ({self.minimax_wins/matches*100:.1f}%)")
        print(f"Draws:    {self.draws}/{matches} ({self.draws/matches*100:.1f}%)")

        majority = max(self.mcts_wins, self.minimax_wins, self.draws)
        print(f"\n{'=' * 50}")
        print("   DETAILED ANALYSIS")
        print(f"{'=' * 50}")

        if self.mcts_wins == majority and self.mcts_wins > self.minimax_wins:
            print("""
    OBSERVATIONS:
      1. MCTS outperformed Minimax at these settings.
      2. Reason: MCTS derives strategy purely from random playouts
          -- no heuristic evaluation function needed.
      3. Random rollouts effectively discovered strong sequences.
      4. Minimax depth-4 was too shallow to reliably counter them.
            """)
        elif self.minimax_wins >= majority:
            print("""
    OBSERVATIONS:
      1. Minimax outperformed MCTS at these settings.
      2. Reason: Connect Four has a known optimal strategy that
         a perfect-information search can exploit.
      3. Minimax's alpha-beta pruning efficiently prunes bad lines.
      4. MCTS with 500 iterations is too few to reliably converge
         for a branching factor of ~7.
            """)
        else:
            print("""
    OBSERVATIONS:
      1. Both algorithms performed similarly.
      2. MCTS: better for games with high branching factor (e.g. Go).
      3. Minimax: better when a strong evaluation function exists.
            """)

        print(f"{'=' * 50}")
        print("   ALGORITHM COMPARISON")
        print(f"{'=' * 50}")
        print("""
    +-------------------+---------------------------+-------------------------+
    | Aspect            | MCTS                      | Minimax                 |
    +-------------------+---------------------------+-------------------------+
    | Heuristics        | None needed               | Requires evaluation fn  |
    | Search type       | Statistical sampling      | Exhaustive (alpha-beta) |
    | Memory            | Grows with iterations     | Fixed depth (DFS)       |
    | Best for          | Complex games (Go, chess) | Simple perfect-info     |
    | Convergence       | Asymptotic to minimax     | Exact within depth      |
    +-------------------+---------------------------+-------------------------+
        """)
