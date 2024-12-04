import pygame
import pygame_menu

class Rectangle():
    
    def __init__(self):
        self.rectState = 0
        self.messageDim = [70, 220, 500, 200]
        self.timer = 100
        self.mode = 0
        self.rect = pygame.Rect(self.messageDim)
    
    def changeSize(self, factor):
        if self.timer != 0:
            self.rect.inflate_ip(factor, 0)
            self.timer = self.timer - 1
        else:
            self.mode = 1
            self.timer = 5
        
    
    def getMessageRect(self):
        padRect = [0, 0, 0, 0]
        for i in range(len(self.messageDim)):
            padRect[i] = self.messageDim[i] + 20
        
        return pygame.Rect(padRect)
    
    
    def renderRectangle(self, screen):
        pygame.draw.rect(screen, pygame.Color("#ffffff"), self.rect, 3) 
        