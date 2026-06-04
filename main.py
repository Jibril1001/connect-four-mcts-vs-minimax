from arena import Arena


def display_explanation():
    print("\n" + "=" * 60)
    print("   MONTE CARLO TREE SEARCH (MCTS) EXPLANATION")
    print("=" * 60)
    print("""
MCTS replaces human-written rules with PURE STATISTICS:

+-----------------------------------------------------------+
| THE 4 PHASES (each iteration):                            |
+-----------------------------------------------------------+
| 1. SELECTION                                              |
|    Traverse tree using UCT formula:                       |
|    UCT = Win_Rate + C * sqrt(ln(parent_visits)/visits)    |
|    This balances EXPLOITATION vs EXPLORATION              |
|                                                           |
| 2. EXPANSION                                              |
|    Add ONE new child node for an untried move             |
|                                                           |
| 3. SIMULATION (Rollout)                                   |
|    Play COMPLETELY RANDOM moves until game ends           |
|    "The AI imagines thousands of possible futures"        |
|                                                           |
| 4. BACKPROPAGATION                                        |
|    Propagate result up the tree, updating win/visit counts|
|    Parents get 'credit' for leading to winning futures    |
+-----------------------------------------------------------+
| KEY INSIGHT:                                              |
| As iterations -> inf, MCTS converges to perfect Minimax!  |
+-----------------------------------------------------------+

CONTENDERS:
[R] MCTS: Statistical simulation, no heuristics needed
[Y] Minimax: Assumes perfect opponent, uses Alpha-Beta pruning
        """)
    input("\nPress Enter to start the battle...")


def main():
    display_explanation()

    arena = Arena()

    print("\n" + "=" * 50)
    print("   BATTLE OPTIONS")
    print("=" * 50)
    print("1. Live Fight (watch one detailed match)")
    print("2. Tournament (10 matches for stats)")
    print("3. Interactive Mode (play against AI)")

    choice = input("\nChoose (1-3): ")

    if choice == '1':
        arena.live_fight()
    elif choice == '2':
        arena.run_tournament(10)
    elif choice == '3':
        arena.interactive_mode()
    else:
        arena.live_fight()

    input("\n\nPress Enter to exit...")


if __name__ == "__main__":
    main()
