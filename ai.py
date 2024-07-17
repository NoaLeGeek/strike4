import math

class Bot:
    def __init__(self, symbol):
        self.symbol = symbol

    def best_move(self, board):
        best_move = (-1, -1)
        best_value = float('-inf')
        for i, j in board.get_empty_spots():
            board.board[i][j].set(self.symbol)
            move_value = board.minimax(0, self.symbol*math.inf, -self.symbol*math.inf, False, self.symbol)
            board.board[i][j].empty()
            if move_value > best_value:
                best_move = (i, j)
                best_value = move_value
        return best_move
