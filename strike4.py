import random
import pygame

class Game:

    # 5x5 board by default
    # Win by having 4 in a row
    # 1 is X, -1 is O, 0 is empty

    def __init__(self, rows=5, columns=5, length_win=4):
        self.rows = rows
        self.columns = columns
        self.length_win = length_win
        self.turn = 1
        self.debug = False
        self.board = Board(self, rows, columns)
    
    def change_turn(self):
        self.turn *= -1

    def best_move(self, symbol=None) -> None:
        board = self.board.board
        best_move = (-1, -1)
        best_value = float('-inf')
        for i in range(self.rows):
            for j in range(self.columns):
                if board[i][j].is_empty():
                    board[i][j].set(symbol)
                    move_value = self.board.minimax(board, 0, float('-inf'), float('inf'), False)
                    board[i][j].empty()
                    if move_value > best_value:
                        best_move = (i, j)
                        best_value = move_value
        return best_move

    def random_move(self, symbol=None):
        empty_spots = self.board.get_empty_spots()
        if empty_spots:
            row, column = random.choice(empty_spots)
            self.board.move(row, column, symbol if symbol else self.turn)
    
    def reset(self):
        self.board = Board(self, self.rows, self.columns)
        self.turn = 1
    
class Board:
    def __init__(self, game, rows=5, columns=5):
        self.game = game
        self.rows = rows
        self.columns = columns
        self.board = [[Tile(row, column) for column in range(columns)] for row in range(rows)]

    def draw(self) -> None:
        pass

    def print(self):
        return "\n".join(["".join([self.board[i][j].convert_symbol() for j in range(self.columns)]) for i in range(self.rows)])

    def move(self, i, j, symbol=None):
        symbol = symbol if symbol else self.turn
        if symbol is None:
            print("im None its not normal")
        self.board[i][j].set(symbol)
        print("Player", self.board[i][j].convert_symbol(), "played at", i, j)
        self.game.change_turn()
    
    def get_empty_spots(self):
        return [(i, j) for i in range(self.rows) for j in range(self.columns) if self.board[i][j].is_empty()]
    
    def is_draw(self) -> bool:
        return all([not self.board[i][j].is_empty() for i in range(self.rows) for j in range(self.columns)])
    
    def check_win(self) -> int:
        # Check if any player has won
        for symbol in [-1, 1]:
            for i in range(self.rows):
                for j in range(self.columns-self.game.length_win+1):
                    row = [self.board[i][j+k].get() for k in range(self.game.length_win)]
                    if sum(row) == symbol*self.game.length_win:
                        return symbol
            for j in range(self.columns):
                for i in range(self.rows-self.game.length_win+1):
                    column = [self.board[i+k][j].get() for k in range(self.game.length_win)]
                    if sum(column) == symbol*self.game.length_win:
                        return symbol
            for i in range(self.rows-self.game.length_win+1):
                for j in range(self.columns-self.game.length_win+1):
                    diagonal1 = [self.board[i+k][j+k].get() for k in range(self.game.length_win)]
                    if sum(diagonal1) == symbol*self.game.length_win:
                        return symbol
                    diagonal2 = [self.board[i+k][j+self.game.length_win-k-1].get() for k in range(self.game.length_win)]
                    if sum(diagonal2) == symbol*self.game.length_win:
                        return symbol
        # Check if the board is full
        if self.is_draw():
            return 0
        return None
    
    def minimax(self, depth, alpha, beta, is_maximizing: True, symbol = None) -> float:
        win = self.check_win()
        if win is not None:
            return win
        symbol = symbol if symbol else self.game.turn
        if symbol is None:
            print("im None its not normal")
        if is_maximizing:
            max_eval = float('-inf')
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j].is_empty():
                        self.board[i][j].set(symbol)
                        eval = self.minimax(self.board, depth + 1, alpha, beta, False)
                        self.board[i][j].empty()
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j].is_empty():
                        self.board[i][j].set(-symbol)
                        eval = self.minimax(self.board, depth + 1, alpha, beta, True)
                        self.board[i][j].empty()
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

class Tile:
    def __init__(self, row, column, object=0):
        self.row = row
        self.column = column
        self.object = object

    def convert_symbol(self) -> str:
        return {1: "X", -1: "O", 0: "-"}[self.object]
    
    def is_empty(self) -> bool:
        return self.object == 0

    def empty(self) -> None:
        self.object = 0

    def is_equal(self, symbol) -> bool:
        return self.object == symbol
    
    def get(self) -> int:
        return self.object
    
    def set(self, symbol) -> None:
        self.object = symbol
    
game = Game()
for _ in range(3):
    game.random_move()
i = 0
win, draw = 0, 0
while game.board.check_win() != 1 and i < 1001:
    print("="*game.columns)
    print(game.board.print())
    print("="*game.columns)
    if game.turn == -1:
        game.best_move()
    else:
        game.random_move()
    print("Winning?", game.board.check_win())
    if game.board.check_win() in [-1, 0]:
        i += 1
        print(i)
        win += game.board.check_win() == -1
        draw += game.board.check_win() == 0
        game.reset()
        for _ in range(3):
            game.random_move()
print("Win:", win, "Draw:", draw)
