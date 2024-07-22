import random
import pygame
import math
from ai import Bot
from game import Game

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