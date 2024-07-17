import pygame

class Label:
    def __init__(self, topleft:tuple[int, int,], text:str, font:pygame.font.Font, color:str):
        self.text = text
        self.topleft = topleft 
        self.font = font 
        self.color = color

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = self.topleft
        screen.blit(text_surface, text_rect)
        