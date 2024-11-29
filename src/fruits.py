import pygame
from src.player import Player

class Fruits():
    def __init__(self, posX, posY, type):
        self.spinTimer = 0
        
        self.fruit = type
        
        self.fruitList = {
            0: pygame.image.load('assets/apple1.png').convert_alpha(),
            1: pygame.image.load('assets/banana.png').convert_alpha(),
            2: pygame.image.load('assets/melon.png').convert_alpha(),
            3: pygame.image.load('assets/orange.png').convert_alpha(),
            4: pygame.image.load('assets/strawberry.png').convert_alpha(),
        }
        
        self.fruitImgPath = self.fruitList[type]
        self.fruitImg = self.fruitImgPath
        
        self.x = posX
        self.y = posY
        self.chargeTimer = 5000
        
        self.rect = 0
        self.state = 0
        self.PlayerVec = [0, 0]
        
    def spin(self, speed):
        if self.spinTimer < 360:
            self.fruitImg = pygame.transform.rotate(self.fruitImgPath, self.spinTimer)
            self.rect = self.fruitImg.get_rect(center = (self.x, self.y))
            self.spinTimer = self.spinTimer + speed
        else:
            self.spinTimer = 0
        
    def charge(self, playerX, playerY, factor):
        if self.chargeTimer != 0:
            self.spin(factor / ((self.chargeTimer) + factor))
            self.chargeTimer = self.chargeTimer - 1
        else:
            self.state = 1
            self.PlayerVec = self.getPlayerVector(playerX, playerY, factor)
    
    
    def getPlayerVector(self, playerX, playerY, factor):
        myVector = []
        myVector.append((playerX - self.x) / factor)
        myVector.append((playerY - self.y) / factor)
        return myVector
    
    def fruitRender(self, screen, playerX, playerY):
        if self.state == 0:
            self.charge(playerX, playerY, 1000)
        else:
            self.spin(0.25)
            self.x = self.x + self.PlayerVec[0]
            self.y = self.y + self.PlayerVec[1]
        screen.blit(self.fruitImg, self.rect)