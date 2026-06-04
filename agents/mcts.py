import math
import random

from engine import ConnectFour, Player


class MCTSNode:
    def __init__(self, state: ConnectFour, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried = state.get_valid_moves()
        self.player = parent.state.current_player if parent else None

    def uct(self, c=math.sqrt(2)):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)


class MCTSAgent:
    def __init__(self, iterations: int = 500):
        self.iterations = iterations

    def _rollout(self, state: ConnectFour) -> Player:
        """Phase 3: SIMULATION (random playout).

        Plays completely random moves from the given state until the
        game ends. Returns the winner (or None for a draw).
        """
        sim = state.clone()
        while not sim.game_over:
            moves = sim.get_valid_moves()
            if moves:
                sim.play_turn(random.choice(moves))
        return sim.winner

    def get_move(self, state: ConnectFour) -> int:
        """Runs MCTS to select the best move.

        Repeats the four-phase cycle (selection, expansion, simulation,
        backpropagation) for self.iterations times, then returns the
        most-visited child of the root.

        Phase 1 - SELECTION:
            Starting from the root, traverse the tree using the UCT
            formula. Always select the child with the highest UCT value
            (the formula itself handles both players via per-node
            win-perspective tracking).

        Phase 2 - EXPANSION:
            When a node with unplayed moves is reached, pick one untried
            move and create a new child node for it.

        Phase 3 - SIMULATION:
            Call _rollout() — play random moves from the new node's
            state until the game ends.

        Phase 4 - BACKPROPAGATION:
            Walk back up from the expanded node to the root, incrementing
            each node's visit count and updating its win total from the
            perspective of the player who made the move leading to it.
        """
        root = MCTSNode(state.clone())

        for _ in range(self.iterations):
            node = root
            while not node.untried and node.children:
                node = max(node.children, key=lambda c: c.uct())

            if node.untried and not node.state.game_over:
                move = node.untried.pop()
                new_state = node.state.clone()
                new_state.play_turn(move)
                node = MCTSNode(new_state, node, move)
                node.parent.children.append(node)

            result = self._rollout(node.state)

            while node:
                node.visits += 1
                if node.player is not None:
                    if result == node.player:
                        node.wins += 1.0
                    elif result is None:
                        node.wins += 0.5
                node = node.parent

        if not root.children:
            return random.choice(state.get_valid_moves())
        return max(root.children, key=lambda c: c.visits).move
