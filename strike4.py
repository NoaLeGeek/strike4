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

    def move_better(self, symbol=None) -> None:
        symbol = symbol if symbol else self.turn
        move = self.board.best_move(symbol)
        if move:
            print("I did the best move at", move)
            self.board.move(*move, symbol)
        else:
            print("I did a random move")
            self.move_randomly(symbol)

    def move_randomly(self, symbol=None):
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

    def score(self) -> int:
        pass

    def draw(self) -> None:
        pass

    def print(self):
        return "\n".join(["".join([self.get(i, j).convert_symbol() for j in range(self.columns)]) for i in range(self.rows)])
    
    def get(self, i, j):
        return self.board[i][j]
    
    def set(self, i, j, symbol):
        self.board[i][j].object = symbol

    def move(self, i, j, symbol=None):
        symbol = symbol if symbol else self.turn
        self.set(i, j, symbol)
        print("Player", self.get(i, j).convert_symbol(), "played at", i, j)
        self.game.change_turn()
    
    def get_empty_spots(self):
        return list(filter(lambda coord: self.get(*coord).is_empty(), self.get_all_coords()))
    
    def is_draw(self) -> bool:
        return all([not self.get(*coord).is_empty() for coord in self.get_all_coords()])
    
    def check_win(self) -> int:
        # Check if any player has won
        for symbol in [-1, 1]:
            for i in range(self.rows):
                for j in range(self.columns-self.game.length_win+1):
                    row = [self.board[i][j+k].object for k in range(self.game.length_win)]
                    if sum(row) == symbol*self.game.length_win:
                        return symbol
            for j in range(self.columns):
                for i in range(self.rows-self.game.length_win+1):
                    column = [self.board[i+k][j].object for k in range(self.game.length_win)]
                    if sum(column) == symbol*self.game.length_win:
                        return symbol
            for i in range(self.rows-self.game.length_win+1):
                for j in range(self.columns-self.game.length_win+1):
                    diagonal1 = [self.board[i+k][j+k].object for k in range(self.game.length_win)]
                    diagonal2 = [self.board[i+k][j+self.game.length_win-k-1].object for k in range(self.game.length_win)]
                    if sum(diagonal1) == symbol*self.game.length_win or sum(diagonal2) == symbol*self.game.length_win:
                        return symbol
        # Check if the board is full
        if self.is_draw():
            return 0
        return None
    
    def best_move(self, symbol=None) -> tuple[int, int]|None:
        symbol = symbol if symbol else self.turn
        coords = self.get_all_coords()
        # Check if the player can win in the next move
        for player in [1, -1]:
            for coord in coords:
                if self.get(*coord).is_empty():
                    self.set(*coord, symbol*player)
                    win = (self.check_win() == symbol*player)
                    self.set(*coord, 0)
                    if win:
                        return coord
        # Check if the player can create a win situation in the next move
        for player in [1, -1]:
            for coord1 in coords:
                if self.get(*coord1).is_empty():
                    self.set(*coord1, symbol*player)
                    count = 0
                    for coord2 in coords:
                        if self.get(*coord2).is_empty():
                            self.set(*coord2, symbol*player)
                            if self.check_win() == symbol*player:
                                count += 1
                            self.set(*coord2, 0)
                            if count > 1:
                                self.set(*coord1, 0)
                                return coord1
                    self.set(*coord1, 0)
        return None
                        
    def get_all_coords(self):
        return [(i, j) for i in range(self.rows) for j in range(self.columns)]

class Tile:
    def __init__(self, row, column, object=0):
        self.row = row
        self.column = column
        self.object = object

    def convert_symbol(self) -> str:
        return {1: "X", -1: "O", 0: "-"}[self.object]
    
    def is_empty(self) -> bool:
        return self.object == 0
    
game = Game()
print(game.board.print())
for _ in range(3):
    game.move_randomly()
i = 0
win, draw = 0, 0
while game.board.check_win() != 1 and i < 1001:
    print("="*game.columns)
    print(game.board.print())
    print("="*game.columns)
    if game.turn == -1:
        game.move_better()
    else:
        game.move_randomly()
    print("Winning?", game.board.check_win())
    if game.board.check_win() in [-1, 0]:
        i += 1
        print(i)
        win += game.board.check_win() == -1
        draw += game.board.check_win() == 0
        game.reset()
        for _ in range(3):
            game.move_randomly()
print("Win:", win, "Draw:", draw)
