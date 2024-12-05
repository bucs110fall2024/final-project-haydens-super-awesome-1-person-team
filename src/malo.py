import pygame
import random
import math
from src.projectiles import Projectiles

class Malo():
    def __init__(self, xPos, yPos, scale, clock):
        """
        Initializes the Malo enemy object
        args:
            - xPos : int - starting x coordinate
            - yPos : int - starting y coordinate
            - scale : float - size of the object's sprite
            - clock : float - game's clock speed (used for some fps independent logic calculation)
        """
        
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
        self.DEFPROJECTILEMULT = 5
    
        self.projectilesAdded = 0
        self.attackNum = random.randint(1, 3)
        #self.attackNum = 3
        self.ATTACKTIMERCONST = 20000
        self.attackTimer1 = self.ATTACKTIMERCONST
        self.attackTimer2 = 0
        
        self.round = 1
        
        self.attackDone = False
        self.backwards = False
        
        self.tailAngle = 0
        self.bodyBounce = 0
        self.bodyAnimBL = 'tail'
        
        
        
        self.canTurn = True
        self.honk = False
        self.HEADTIMER = 5000
        self.currentTurnTimer = 5000
        self.animTimer = 0
        
    def imageSetup(self, oldDic, newDic):
        """
        Sets up all of Malo's sprites and stores the new pygame surfaces in it's own dictionary to save computing time of loading the file
        on each render.
        args:
            - oldDic : dictionary (int, string) - the dictionary with all the image paths
            - newDic : dictionary (int, pygame surface) - the new dictionary that will have all the pygame surfaces for each of the image paths
        return: none
        """
        for part, path in oldDic.items():
            original_image = pygame.image.load(path).convert_alpha() 
            scaled_image = pygame.transform.scale(original_image, (self.size, self.size))
            newDic[part] = scaled_image
    
    def nakulaAttack(self):
        """
        Handles the nakula attack, where baby proboscis monkeys can be seen falling down from the top of the screen, as well as jumping from the
        bottom of the screen
        args: none
        return: none
        """
        if self.projectileMult == 5:
           projInterval = 1000 - (50 * self.projectileMult) 
        else:
           projInterval = 1000 - (40 * self.projectileMult)
        
        spacing = 540 / self.projectileMult
        
        if self.attackTimer2 - self.lastProjSpawn > projInterval:
            self.lastProjSpawn = self.attackTimer2
            if self.projectilesAdded % 2:
                self.projectiles.append(Projectiles((spacing * self.projectilesAdded), 420, 5, self.deltaTime, 0, 2))
            else:
                self.projectiles.append(Projectiles((spacing * self.projectilesAdded), -50, 5, self.deltaTime, 0, 1))
                print("hello")
            if self.backwards == False:
                self.projectilesAdded += 1
            if self.projectilesAdded == self.projectileMult + 1 or self.backwards == True:
                self.backwards = True
                self.projectilesAdded -= 1
            if self.projectilesAdded == 0 and self.backwards == True:
                self.backwards = False
    
    def ehAttack(self):
        """
        Handles the 'eh' attack, where a bunch of projectiles with a 'eh' text sprite can be seen moving from the left of the screen in a wave
        at the player, each with a unique offset to reduce cheese
        args: none
        return: none
        """
        if self.projectileMult == 15:
            projInterval = 1000 - (10 * self.projectileMult) 
        else:
            projInterval = 1000 - (30 * self.projectileMult) 

        if self.attackTimer2 - self.lastProjSpawn > projInterval:
            self.lastProjSpawn = self.attackTimer2
            for i in range(4):
                if i % 2 == 0:
                    self.projectiles.append(Projectiles(-50, 30 + (i * (150 - (self.projectileMult))), 6, self.deltaTime, self.projectileMult, 2, math.radians(random.randint(0, 180))))
                else:
                    self.projectiles.append(Projectiles(-50, 30 + (i * (150 - (self.projectileMult))), 6, self.deltaTime, self.projectileMult, 1, math.radians(random.randint(0, 180))))  
            
    def fruitAttack(self):
        """
        Handles the fruit attack, where a bunch of fruits will spawn near the top middle of the screen, spin, then charge at wherever the player's position
        at that moment was.
        args: none
        return: none
        """
        spacing = 540 / self.projectileMult
        if self.projectileMult != 15:
           projInterval = 1000 - (75 * self.projectileMult) 
        else:
           projInterval = 1000 - (50 * self.projectileMult)
        if self.attackTimer2 - self.lastProjSpawn > projInterval and self.attackDone == False:
            self.lastProjSpawn = self.attackTimer2
           
            
            self.projectiles.append(Projectiles(spacing + (spacing * self.projectilesAdded), 75, random.randint(0, 4), self.deltaTime))
            self.projectilesAdded += 1
            if self.projectilesAdded == self.projectileMult:
               self.attackDone = True
               
            
               
        if self.attackDone == True and self.attackTimer2 - self.lastProjSpawn > (self.projectileMult * projInterval):
            self.projectilesAdded = 0
            self.attackDone = False   
        
    def handleAttacks(self, screen, player):
        """
        Handles all attacks of all categories, and ensures that when the attack timer goes back to 0, that all necessary variables are reset. Also
        handles projectile garbage collection if projectile goes farther than what is visible.
        args: none
        return: none
        """
        if self.attackTimer1 <= 0:
            self.attackTimer1 = self.ATTACKTIMERCONST
            for projectile in list(self.projectiles):
                self.projectiles.remove(projectile)
            self.attackNum = random.randint(1, 3)
            #self.attackNum = 3
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
                
            if self.attackNum == 3:
                self.ehAttack()
                
            for projectile in self.projectiles:
                projectile.projectileRender(screen, player.x, player.y)
                if projectile.y > 600 or projectile.x > 800 or projectile.x < -200:
                    self.projectiles.remove(projectile)

            self.attackTimer1 -= 1 * self.deltaTime
            self.attackTimer2 += 1 * self.deltaTime
    
    def animateMalo(self):
        """
        Runs functions that handles animations for parts of Malo
        args: none
        return: dictionary (string, pygame surface) - a dictionary of animated parts to draw gathered from the animation functions
        """
        animatedParts = {}
        animatedTail = self.tailAnimate()
        body = self.bodyAnimate()
        
        
        
        animatedParts['tail'] = animatedTail
        animatedParts.update(body)
        #animatedParts['head'] = head
        
        
        
        return animatedParts
        
    def tailAnimate(self):
        """
        Handles animating Malo's tail
        args: none
        return: pygame surface - the tail's sprite image taken into account it's current animation frame
        """
        self.tailAngle = (self.tailAngle + 1) % 360
        rotated_tail = pygame.transform.rotate(self.parts['tail'], self.bounceAnim(20, 1, self.tailAngle))  
        self.rects['tail'] = rotated_tail.get_rect(center = self.parts['tail'].get_rect(topleft = (self.x, self.y)).center)  
        
        
        return rotated_tail
    
    def bounceAnim(self, amp, freq, var, func = 'sin' ):
        """
        Useful but otherwise lengthy trig functions that are used to animate Malo
        args:
            - amp : int - the amplitude of the wave
            - freq : int - the frequency of the wave
            - var : int - basically the 'x' of the equation, is what actually is inputted into the trig equation
            - func: string- the specified trig function to use
        return: float - result
        """
        if func == 'sin':
            return amp * math.sin(freq * math.radians(var))
        else:
            return amp * math.cos(freq * math.radians(var))
    
    def headAnimate(self):
        """
        Handles animating Malo's head as well as the chance for Malo to look at the player and 'honk'
        args: none
        return: pygame Surface - the animated image with respect to animation frame and sprite
        """
        
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
        """
        Handles animating the rest of Malo's body besides head and tail. However the head animation function is called here to 'mix' both animations
        args: none
        return: dictionary (string, pygame surface) - returns a dictionary that has all of the body part surfaces being animated as well as it's name
        """
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
        """
        Handles the drawing of all of Malo's sprites
        args:
            - screen : pygame Surface object - the whole game screen
        return: none
        """
        
        animatedParts = self.animateMalo()

        for part in animatedParts:
            
            screen.blit(animatedParts[part], self.rects[part])
        
        
            
    def difficultyStats(self, difficulty):
        """
        Called whenever difficulty is changed; Sets projectile multiplier
        args: none
        return: none
        """
        self.projectileMult = self.DEFPROJECTILEMULT * difficulty
        
    