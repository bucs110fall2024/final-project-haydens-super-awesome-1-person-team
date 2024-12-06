import pygame
import math

class Projectiles():
    def __init__(self, xPos, yPos, type, clock, difficulty=0, projType=0, offset=0):
        """
        Initializes a projectile object
        args:
            - xPos : int - starting x coordinate
            - yPos : int - starting y coordinate
            - type : int - projectiles' sprite classification
            - clock : float - game's clock speed (used for some fps independent logic calculation)
            - difficulty : int - game's current difficulty
            - projType : int - classification of a sprite's behavior (within the same sprite)
            - offset : int - used for the 'Eh' attack's unique offsets
        """
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
        
        if projType == 1:
            self.projImg = pygame.transform.flip(self.projImg, False, True)
        
            
        
        self.x = xPos
        self.y = yPos
        
        self.ORIGX = xPos
        self.ORIGY = yPos
        
        self.Timer = 150
        
        self.difficulty = difficulty
        
        self.deltaTime = clock
        
        self.projBehavior = projType
        self.curSpeed = 0
        self.ACCEL = 10
        self.animProj = self.projImg
        self.offset = offset
        
        self.rect = self.projImg.get_rect(topleft = (self.x, self.y))
        self.hitbox = self.projImg.get_rect(center = self.projImg.get_rect(topleft = (self.x, self.y)).center).scale_by(0.5)
        self.state = 0
        self.PlayerVec = [0, 0]
        
        
    def spin(self, speed):
        """
        spin the projectile
        args:
            - speed : float - the speed to spin the projectile
        return: none
        """  
        self.spinTimer = (self.spinTimer + speed) % 360
        
        spunObject = pygame.transform.rotate(self.projImg, self.spinTimer * self.deltaTime)
        self.rect = spunObject.get_rect(center = self.projImg.get_rect(topleft = (self.x, self.y)).center)
        
        self.animProj = spunObject
        
    def fruitHandle(self, playerX, playerY, factor):
        """
        handles the fruit attack behavior
        args:
            - playerX : float - the x position of the player
            - playerY : float - the y position of the player
            - factor : int - the multiplier for the speed of the fruit
        return: none
        """  
        if self.Timer != 0:
            self.spin(factor / ((self.Timer) + factor))
            self.Timer = self.Timer - 1
        else:
            self.state = 1
            self.PlayerVec = self.getPlayerVector(playerX, playerY, factor)
            
    def nakulaHandle(self):
        """
        handles the nakula attack behavior
        args: none
        return: none
        """  
        if self.projBehavior == 1:
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
            
    def ehHandle(self):
        """
        handles the 'eh' attack behavior
        args: none
        return: none
        """  
        freq = self.difficulty / 3
        if self.difficulty == 15:
            speed = self.difficulty / 20
        else:
            speed = self.difficulty / 10
        if self.projBehavior < 3:
            if self.projBehavior == 1:
                self.y = (50 * math.sin((freq * math.radians(self.Timer)) + self.offset)) + self.ORIGY    
            if self.projBehavior == 2:
                self.y = (50 * math.cos((freq * math.radians(self.Timer)) + self.offset)) + self.ORIGY    
            self.x += 0.3 * self.deltaTime * speed
            
        
            
        self.rect = self.projImg.get_rect(center = self.projImg.get_rect(topleft = (self.x, self.y)).center)
        
        self.Timer += 1
            
                    
        
        
    
    
    def getPlayerVector(self, playerX, playerY, factor):
        """
        gets the player's position and makes a list out of it with respect to the projectiles' own position
        args:
            - playerX : float - the x position of the player
            - playerY : float - the y position of the player
            - factor : int - the scale for the vector
        return: list (float), list of coordinates of how the fruit should move each tick
        """  
        myVector = []
        myVector.append((playerX - self.x) / 1000)
        myVector.append((playerY - self.y) / 1000)
        return myVector
    
    def projectileRender(self, screen, playerX, playerY):
        """
        handles drawing the projectiles
        args:
            - screen : pygame Surface object - the whole game screen
            - playerX : float - the x position of the player
            - playerY : float - the y position of the player
        return: none
        """  
        if self.type <= 4:
            if self.state == 0:
                self.fruitHandle(playerX, playerY, 50)
            else:
                self.spin(1)
                self.x += self.PlayerVec[0]  * self.deltaTime
                self.y += self.PlayerVec[1]  * self.deltaTime  
        elif self.type == 5:
            if self.state == 0:
                self.nakulaHandle()
        else:
            self.ehHandle()
        self.hitbox = self.projImg.get_rect(center = self.projImg.get_rect(topleft = (self.x, self.y)).center).scale_by(0.8)     
        screen.blit(self.animProj, self.rect)
        