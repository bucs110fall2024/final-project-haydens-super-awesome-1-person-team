import pygame
import pyganim
from src.rectangle import Rectangle

class Player():
    def __init__(self, xPos, yPos):
        self.playerState = 0
        self.speed = 0.25
        self.x = xPos
        self.y = yPos
        self.playerImage = pygame.image.load('assets/player.png').convert_alpha()
        self.myBox = self.playerImage.get_rect()
        self.collisionGrid = [True, True, True, True]
        self.health = 50
        
        
        
    def isColliding(self, rect):
        collision = []
        if self.x + self.myBox.width >= rect.right:
            collision.append(False)
        else:
            collision.append(True)
        if self.x <= rect.left:
            collision.append(False)
        else:
            collision.append(True)
        if self.y <= rect.top:
            collision.append(False)
        else:
            collision.append(True)
        if self.y + self.myBox.height >= rect.bottom:
            collision.append(False)
        else:
            collision.append(True)
            
        return collision
    
        
        
    def handlePlayer(self, keys, rect):
        self.collisionGrid = self.isColliding(rect)
        if self.collisionGrid[2]:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.y = self.y - self.speed
        if self.collisionGrid[3]:
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.y = self.y + self.speed
        if self.collisionGrid[0]:
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.x = self.x + self.speed
        if self.collisionGrid[1]:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.x = self.x - self.speed
        
    def renderPlayer(self, screen):
        screen.blit(self.playerImage, [self.x, self.y])