import random
from typing import Optional, Tuple

from engine import ConnectFour, Player


class MinimaxAgent:
    def __init__(self, player: Player, depth: int = 4):
        self.player = player
        self.opponent = Player.YELLOW if player == Player.RED else Player.RED
        self.depth = depth

    def _evaluate(self, state: ConnectFour) -> int:
        score = 0
        board = state.board

        for row in range(state.rows):
            if board[row][3] == self.player.value:
                score += 3

        def eval_window(window):
            if window.count(self.player.value) == 4:
                return 100
            if window.count(self.player.value) == 3 and window.count(0) == 1:
                return 10
            if window.count(self.player.value) == 2 and window.count(0) == 2:
                return 5
            if window.count(self.opponent.value) == 3 and window.count(0) == 1:
                return -8
            return 0

        for r in range(state.rows):
            for c in range(state.cols - 3):
                window = [board[r][c + i] for i in range(4)]
                score += eval_window(window)

        for c in range(state.cols):
            for r in range(state.rows - 3):
                window = [board[r + i][c] for i in range(4)]
                score += eval_window(window)

        return score

    def _minimax(
        self, state: ConnectFour, depth: int, alpha: float, beta: float, is_max: bool
    ) -> Tuple[float, Optional[int]]:
        if depth == 0 or state.game_over:
            if state.winner == self.player:
                return 1e6, None
            if state.winner == self.opponent:
                return -1e6, None
            return self._evaluate(state), None

        moves = state.get_valid_moves()
        if not moves:
            return 0, None

        if is_max:
            best_score = -float('inf')
            best_move = moves[0]
            for move in moves:
                new_state = state.clone()
                new_state.play_turn(move)
                score, _ = self._minimax(new_state, depth - 1, alpha, beta, False)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = moves[0]
            for move in moves:
                new_state = state.clone()
                new_state.play_turn(move)
                score, _ = self._minimax(new_state, depth - 1, alpha, beta, True)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score, best_move

    def get_move(self, state: ConnectFour) -> int:
        _, move = self._minimax(state, self.depth, -float('inf'), float('inf'), True)
        return move if move is not None else random.choice(state.get_valid_moves())
