from arena import Arena


def display_explanation():
    print("\n" + "=" * 60)
    print("   MONTE CARLO TREE SEARCH (MCTS) EXPLANATION")
    print("=" * 60)
    print("""
MCTS replaces human-written rules with PURE STATISTICS:

┌─────────────────────────────────────────────────────────────┐
│ THE 4 PHASES (each iteration):                              │
├─────────────────────────────────────────────────────────────┤
│ 1. SELECTION                                                │
│    Traverse tree using UCT formula:                         │
│    UCT = Win_Rate + C × √(ln(parent_visits)/node_visits)    │
│    This balances EXPLOITATION (known wins) vs EXPLORATION   │
│                                                             │
│ 2. EXPANSION                                                │
│    Add ONE new child node for an untried move               │
│                                                             │
│ 3. SIMULATION (Rollout)                                     │
│    Play COMPLETELY RANDOM moves until game ends             │
│    "The AI imagines thousands of possible futures"          │
│                                                             │
│ 4. BACKPROPAGATION                                          │
│    Propagate result up the tree, updating win/visit counts  │
│    Parents get 'credit' for leading to winning futures      │
├─────────────────────────────────────────────────────────────┤
│ KEY INSIGHT:                                                │
│ As iterations → ∞, MCTS converges to perfect Minimax!       │
└─────────────────────────────────────────────────────────────┘

CONTENDERS:
🔴 MCTS: Statistical simulation, no heuristics needed
🟡 Minimax: Assumes perfect opponent, uses Alpha-Beta pruning
        """)
    input("\nPress Enter to start the battle...")


def main():
    display_explanation()

    arena = Arena()

    print("\n" + "=" * 50)
    print("   BATTLE OPTIONS")
    print("=" * 50)
    print("1. ⚔️ Single Match (watch one fight)")
    print("2. 🏆 Tournament (10 matches for stats)")

    choice = input("\nChoose (1-2): ")

    if choice == '1':
        arena.run_match(verbose=True)
    elif choice == '2':
        arena.run_tournament(10)
    else:
        arena.run_match(verbose=True)

    input("\n\nPress Enter to exit...")


if __name__ == "__main__":
    main()
