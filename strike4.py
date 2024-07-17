import random
import pygame
import math
from config import Config
from ai import Bot

class Game:

    # 5x5 board by default
    # Win by having 4 in a row
    # 1 is X, -1 is O, 0 is empty

    def __init__(self, config: Config) -> None:
        self.turn = 1
        self.debug = False
        self.board = Board(self, config)
        self.bot = Bot(1)
    
    def change_turn(self):
        self.turn *= -1

    def best_move(self, symbol=None) -> None:
        symbol = symbol if symbol else self.turn
        board = self.board.board
        best_move = (-1, -1)
        best_value = float('-inf')
        for i in range(self.rows):
            for j in range(self.columns):
                if board[i][j].is_empty():
                    board[i][j].set(symbol)
                    move_value = self.board.minimax(0, float('-inf'), float('inf'), False, symbol)
                    board[i][j].empty()
                    if move_value > best_value:
                        best_move = (i, j)
                        best_value = move_value
        return self.board.move(*best_move, symbol)

    def random_move(self, symbol=None):
        empty_spots = self.board.get_empty_spots()
        if empty_spots:
            row, column = random.choice(empty_spots)
            self.board.move(row, column, symbol if symbol else self.turn)
    
    def reset(self):
        self.board = Board(self, self.rows, self.columns)
        self.turn = 1
    
class Board:
    def __init__(self, game, config: Config):
        self.game = game
        self.config = config
        self.board = [Tile(row, column) for row, column in self.get_all_coords()]

    def draw(self) -> None:
        pass

    def get_all_coords(self) -> list:
        return [(i, j) for i in range(self.config.rows) for j in range(self.config.columns)]

    def print(self):
        return "\n".join(["".join([self.board[i][j].convert_symbol() for j in range(self.columns)]) for i in range(self.rows)])

    def move(self, i, j, symbol=None):
        symbol = symbol if symbol else self.turn
        self.board[i][j].set(symbol)
        print("Player", self.board[i][j].convert_symbol(), "played at", i, j)
        self.game.change_turn()
    
    def get_empty_spots(self):
        return [(i, j) for i, j in self.get_all_coords() if self.board[i][j].is_empty()]
    
    def is_draw(self) -> bool:
        return all([not self.board[i][j].is_empty() for i, j in self.get_all_coords()])
    
    # Return 1 if X wins, -1 if O wins, 0 if draw, None if game is not over
    def check_win(self) -> int:
        # Check if any player has won
        for symbol in [-1, 1]:
            for i in range(self.rows):
                for j in range(self.columns - self.config.length_win+1):
                    row = [self.board[i][j+k].get() for k in range(self.config.length_win)]
                    if sum(row) == symbol*self.config.length_win:
                        return symbol
            for j in range(self.columns):
                for i in range(self.rows - self.config.length_win+1):
                    column = [self.board[i+k][j].get() for k in range(self.config.length_win)]
                    if sum(column) == symbol*self.config.length_win:
                        return symbol
            for i in range(self.rows - self.config.length_win+1):
                for j in range(self.columns - self.config.length_win+1):
                    diagonal1 = [self.board[i+k][j+k].get() for k in range(self.config.length_win)]
                    if sum(diagonal1) == symbol*self.config.length_win:
                        return symbol
                    diagonal2 = [self.board[i+k][j+self.config.length_win-k-1].get() for k in range(self.config.length_win)]
                    if sum(diagonal2) == symbol*self.config.length_win:
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
        if is_maximizing:
            max_eval = -math.inf
            for i, j in self.get_empty_spots():
                self.board[i][j].set(symbol)
                eval = self.minimax(depth + 1, alpha, beta, False, symbol)
                self.board[i][j].empty()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for i, j in self.get_empty_spots():
                self.board[i][j].set(-symbol)
                eval = self.minimax(depth + 1, alpha, beta, True, -symbol)
                self.board[i][j].empty()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

class Tile:
    def __init__(self, row, column, symbol=0):
        self.row = row
        self.column = column
        self.symbol = symbol

    def convert_symbol(self) -> str:
        return {1: "X", -1: "O", 0: "-"}[self.symbol]
    
    def is_empty(self) -> bool:
        return self.symbol == 0

    def empty(self) -> None:
        self.symbol = 0

    def is_equal(self, symbol) -> bool:
        return self.symbol == symbol
    
    def get(self) -> int:
        return self.symbol
    
    def set(self, symbol) -> None:
        self.symbol = symbol
    
game = Game()
for _ in range(3):
    game.random_move()
i = 0
win, draw = 0, 0
while game.board.check_win() != 1 and i < 2:
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