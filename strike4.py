import random
import pygame
import math
from bot import Bot
from config import Config
from game import Game
from scene import SceneManager


def main():
    pygame.init()
    config = Config()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Strike 4")
    clock = pygame.time.Clock()
    manager = SceneManager()
    game = Game()
    if config.strike4:
        for _ in range(3):
            game.random_move()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            game.handle_event(event)
        game.update()
        game.render(screen)
        pygame.display.flip()
        clock.tick(60)

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