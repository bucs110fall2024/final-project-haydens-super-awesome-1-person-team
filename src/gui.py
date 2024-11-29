import pygame
from src.player import Player

class Gui():
    def __init__(self):
        self.healthDim = [270, 430, 100, 40]
        self.healthB = pygame.Rect(self.healthDim)
        self.healthF = pygame.Rect(self.healthDim)
        
        
        self.font = pygame.font.Font('assets/fight-mono.ttf', 30)
        self.white = pygame.Color('#ffffff')
        
        self.hp = self.font.render("HP", True, self.white)
        self.total = self.font.render("/100", True, self.white)
        self.current = self.font.render("100", True, self.white)
        
    
    def renderHealth(self, screen, health):
        self.healthDim[2] = health
        screen.blit(self.hp, [230, 430])
        screen.blit(self.total, [450, 430])
        screen.blit(self.font.render(str(health), True, self.white), [385, 430])
        pygame.draw.rect(screen, pygame.Color("#ff0000"), self.healthB)
        pygame.draw.rect(screen, pygame.Color("#ffff00"), pygame.Rect(self.healthDim)) 