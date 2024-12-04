import pygame
from src.player import Player

class Projectiles():
    def __init__(self, posX, posY, type, clock, nakulaType=0):
        self.spinTimer = 0
        
        self.type = type
        
        self.projectileList = {
            0: pygame.image.load('assets/apple1.png').convert_alpha(),
            1: pygame.image.load('assets/banana.png').convert_alpha(),
            2: pygame.image.load('assets/melon.png').convert_alpha(),
            3: pygame.image.load('assets/orange.png').convert_alpha(),
            4: pygame.image.load('assets/strawberry.png').convert_alpha(),
            5: pygame.image.load('assets/nakulaBody.png').convert_alpha(),
            6: pygame.image.load('assets/eh1.png').convert_alpha(),
        }
        
        self.projImgPath = self.projectileList[type]
        self.projImg = self.projImgPath
        
        if nakulaType == 1:
            self.projImg = pygame.transform.flip(self.projImg, False, True)
        
            
        
        self.x = posX
        self.y = posY
        self.chargeTimer = 150
        
        self.deltaTime = clock
        
        self.nakulaPos = nakulaType
        self.curSpeed = 0
        self.ACCEL = 10
        self.animProj = self.projImg
        
        self.rect = self.projImg.get_rect(topleft = (self.x, self.y))
        self.state = 0
        self.PlayerVec = [0, 0]
        
    def spin(self, speed):
        
        self.spinTimer = (self.spinTimer + speed) % 360
        
        spunObject = pygame.transform.rotate(self.projImg, self.spinTimer * self.deltaTime)
        self.rect = spunObject.get_rect(center = self.projImg.get_rect(topleft = (self.x, self.y)).center)
        
        self.animProj = spunObject
        
    def fruitCharge(self, playerX, playerY, factor):
        if self.chargeTimer != 0:
            self.spin(factor / ((self.chargeTimer) + factor))
            self.chargeTimer = self.chargeTimer - 1
        else:
            self.state = 1
            self.PlayerVec = self.getPlayerVector(playerX, playerY, factor)
            
    def nakulaHandle(self):
        if self.nakulaPos == 1:
            self.y += self.curSpeed * self.deltaTime
            self.spin(self.curSpeed)
            if self.curSpeed <= 0.01:
                self.curSpeed += 0.0005
            else:
                self.curSpeed += 0.01
        else:
            if self.state == 0:
                self.y += self.curSpeed * self.deltaTime
                self.curSpeed += 0.0005
                if self.curSpeed >= 0.03:
                    self.curSpeed += 0.8
                    self.y -= self.curSpeed * self.deltaTime
                    
            self.rect = self.projImg.get_rect(center = self.projImg.get_rect(topleft = (self.x, self.y)).center)
                    
        
        
    
    
    def getPlayerVector(self, playerX, playerY, factor):
        myVector = []
        myVector.append((playerX - self.x) / 1000)
        myVector.append((playerY - self.y) / 1000)
        return myVector
    
    def projectileRender(self, screen, playerX, playerY):
        if self.type <= 4:
            if self.state == 0:
                self.fruitCharge(playerX, playerY, 50)
            else:
                self.spin(1)
                self.x += self.PlayerVec[0]  * self.deltaTime
                self.y += self.PlayerVec[1]  * self.deltaTime  
        else:
            if self.state == 0:
                #self.spin(0.25)
                self.nakulaHandle()     
        screen.blit(self.animProj, self.rect)
        