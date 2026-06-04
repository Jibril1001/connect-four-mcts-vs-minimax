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

    def uct(self, c=math.sqrt(2)):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)


class MCTSAgent:
    def __init__(self, player: Player, iterations: int = 500):
        self.player = player
        self.iterations = iterations

    def _rollout(self, state: ConnectFour) -> float:
        sim = state.clone()
        while not sim.game_over:
            moves = sim.get_valid_moves()
            if moves:
                sim.play_turn(random.choice(moves))
        if sim.winner == self.player:
            return 1.0
        elif sim.winner is None:
            return 0.5
        return 0.0

    def get_move(self, state: ConnectFour) -> int:
        root = MCTSNode(state.clone())

        for _ in range(self.iterations):
            node = root
            while not node.untried and node.children:
                if node.state.current_player == self.player:
                    node = max(node.children, key=lambda c: c.uct())
                else:
                    node = min(node.children, key=lambda c: c.uct())

            if node.untried and not node.state.game_over:
                move = node.untried.pop()
                new_state = node.state.clone()
                new_state.play_turn(move)
                node = MCTSNode(new_state, node, move)
                node.parent.children.append(node)

            result = self._rollout(node.state)

            while node:
                node.visits += 1
                node.wins += result
                node = node.parent

        if not root.children:
            return random.choice(state.get_valid_moves())
        return max(root.children, key=lambda c: c.visits).move
