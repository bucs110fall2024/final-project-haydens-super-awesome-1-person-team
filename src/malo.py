import pygame
import pyganim
import random
import math
from src.projectiles import Projectiles

class Malo():
    def __init__(self, xPos, yPos, scale, clock):
        self.size = scale
        
        self.partPaths = {
            "tail": 'assets/maloTail.png',
            "lArm": 'assets/malolArm.png',
            "lLeg": 'assets/malolLeg.png',
            "body": 'assets/maloBody.png',
            "rLeg": 'assets/malorLeg.png',
            "rArm": 'assets/malorArm.png',
            "head": 'assets/maloHead.png',
            
        }
        
        self.headExpressionPaths = {
            1: 'assets/maloHead1.png',
            2: 'assets/maloHead2.png',
            3: 'assets/maloHead3.png'
        }
        
        
        self.lastProjSpawn = 0
        self.projInterval = 1000
        
        self.x = xPos
        self.y = yPos
        
        self.rects = {}
        self.parts = {}
        self.headExpressions = {}
            
        self.imageSetup(self.partPaths, self.parts)
        self.imageSetup(self.headExpressionPaths, self.headExpressions)
            
        for part in self.parts :
            self.rects[part] = self.parts[part].get_rect(topleft = (self.x, self.y))
        
        
        
        self.deltaTime = clock
        self.otherTimer = 0
        
        self.projectiles = []
        
        self.projectileMult = 5
        self.defProjectileMult = 5
    
        self.projectilesAdded = 0
        self.attackNum = random.randint(1, 2)
        #self.attackNum = 2
        self.ATTACKTIMERCONST = 20000
        self.attackTimer1 = self.ATTACKTIMERCONST
        self.attackTimer2 = 0
        
        self.round = 1
        
        self.attackDone = False
        self.backwards = False
        
        self.tailAngle = 0
        self.bodyBounce = 0
        self.bodyAnimBL = ['tail']
        
        
        
        self.canTurn = True
        self.honk = False
        self.HEADTIMER = 5000
        self.currentTurnTimer = 5000
        self.animTimer = 0
        
    def imageSetup(self, oldDic, newDic):
        for part, path in oldDic.items():
            original_image = pygame.image.load(path).convert_alpha() 
            scaled_image = pygame.transform.scale(original_image, (self.size, self.size))
            newDic[part] = scaled_image
    
    
    def nakulaAttack(self):
        if self.projectileMult == 5:
           projInterval = 1000 - (50 * self.projectileMult) 
        else:
           projInterval = 1000 - (40 * self.projectileMult)
        
        spacing = 540 / self.projectileMult
        
        if self.attackTimer2 - self.lastProjSpawn > projInterval and self.attackDone == False:
            self.lastProjSpawn = self.attackTimer2
            if self.projectilesAdded % 2:
                self.projectiles.append(Projectiles((spacing * self.projectilesAdded), 420, 5, self.deltaTime, 2))
            else:
                self.projectiles.append(Projectiles((spacing * self.projectilesAdded), -50, 5, self.deltaTime, 1))
            if self.backwards == False:
                self.projectilesAdded += 1
            if self.projectilesAdded == self.projectileMult + 1 or self.backwards == True:
                self.backwards = True
                self.projectilesAdded -= 1
            if self.projectilesAdded == 0 and self.backwards == True:
                self.backwards = False
            
        
    def fruitAttack(self):
        if self.projectileMult != 15:
           projInterval = 1000 - (75 * self.projectileMult) 
        else:
           projInterval = 1000 - (50 * self.projectileMult)
        if self.attackTimer2 - self.lastProjSpawn > projInterval and self.attackDone == False:
            self.lastProjSpawn = self.attackTimer2
           
            spacing = 540 / self.projectileMult
            self.projectiles.append(Projectiles(spacing + (spacing * self.projectilesAdded), 75, random.randint(0, 4), self.deltaTime))
            self.projectilesAdded += 1
            if self.projectilesAdded == self.projectileMult:
               self.attackDone = True
               
            
               
        if self.attackDone == True and self.attackTimer2 - self.lastProjSpawn > (self.projectileMult * projInterval):
            self.projectilesAdded = 0
            self.attackDone = False   
            
           
               
        
        
        
               
        
        
    def handleAttacks(self, screen, player):
        if self.attackTimer1 <= 0:
            self.attackTimer1 = self.ATTACKTIMERCONST
            for projectile in list(self.projectiles):
                self.projectiles.remove(projectile)
            self.attackNum = random.randint(1, 2)
            self.attackDone = False
            self.projectilesAdded = 0
            self.backwards = False
            player.currentScore += 1
            self.round += 1
        
        if self.attackTimer1 > 0:
                
            if self.attackNum == 1:
                self.fruitAttack()
                
                
            if self.attackNum == 2:
                self.nakulaAttack()
                
            for projectile in self.projectiles:
                projectile.projectileRender(screen, player.x, player.y)
                if projectile.y > 600 or projectile.x > 800 or projectile.x < -200:
                    self.projectiles.remove(projectile)

            self.attackTimer1 -= 1 * self.deltaTime
            self.attackTimer2 += 1 * self.deltaTime
               
    def preAttack(self):
        pass
    
    def animateMalo(self, screen):
        animatedParts = {}
        animatedTail = self.tailAnimate()
        body = self.bodyAnimate()
        
        
        
        animatedParts['tail'] = animatedTail
        animatedParts.update(body)
        #animatedParts['head'] = head
        
        
        
        return animatedParts
        
    def tailAnimate(self):
        self.tailAngle = (self.tailAngle + 1) % 360
        rotated_tail = pygame.transform.rotate(self.parts['tail'], self.bounceAnim(20, 1, self.tailAngle))  
        self.rects['tail'] = rotated_tail.get_rect(center = self.parts['tail'].get_rect(topleft = (self.x, self.y)).center)  
        
        
        return rotated_tail
    
    def bounceAnim(self, amp, freq, var, func = 'sin' ):
        if func == 'sin':
            return amp * math.sin(freq * math.radians(var))
        else:
            return amp * math.cos(freq * math.radians(var))
    
    def headAnimate(self):
        
        if self.canTurn:
            currentHead = self.parts['head']
            animHead = pygame.transform.rotate(currentHead, self.bounceAnim(2, 2, self.tailAngle))
        if random.randint(1, 600) == 600 and self.canTurn:
            self.canTurn = False
        if self.canTurn == False:
            if self.animTimer <= 0:
                currentHead = self.headExpressions[2]
                if random.randint(1, 200) == 200:
                    self.honk = True
                    self.animTimer = 500
            if self.animTimer > 0:
                currentHead = self.headExpressions[3]
                self.animTimer -= 1 * self.deltaTime
            self.currentTurnTimer -= 1 * self.deltaTime
            animHead = pygame.transform.rotate(currentHead, self.bounceAnim(10, 2, self.tailAngle))
            if self.currentTurnTimer < 0:
                self.canTurn = True
                self.currentTurnTimer = self.HEADTIMER
                
        
        
        self.rects['head'] = animHead.get_rect(center = self.parts['head'].get_rect(topleft = (self.x, self.y)).center) 
        
        return animHead
    
    def bodyAnimate(self):
        
        animatedBodyParts = {}
        for part in self.parts:
            if part in self.bodyAnimBL:
                continue
            original = self.parts[part]
            bodyPart = pygame.transform.scale(original, [original.get_width() + (5 * math.sin(5 * math.radians(self.tailAngle))), original.get_height() + (5 * math.cos(5 * math.radians(self.tailAngle)))])
            self.rects[part] = bodyPart.get_rect(center = self.parts['body'].get_rect(topleft = (self.x, self.y)).center)  
            
            if part == 'head':
                animatedBodyParts[part] = self.headAnimate()
            else:
                animatedBodyParts[part] = bodyPart
        return animatedBodyParts
    
    
        
           
        
    def renderMalo(self, screen):
        animatedParts = self.animateMalo(screen)

        for part in animatedParts:
            
            screen.blit(animatedParts[part], self.rects[part])
        
        
            
    def difficultyStats(self, difficulty):
        self.projectileMult = self.defProjectileMult * difficulty
        
    
    def intro(self):
        pass
    