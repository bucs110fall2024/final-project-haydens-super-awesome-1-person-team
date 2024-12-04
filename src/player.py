import pygame
import json
from src.rectangle import Rectangle

class Player():
    def __init__(self, xPos, yPos, clock):
        self.playerState = 0
        self.speed = 0.35
        self.x = xPos
        self.y = yPos
        self.playerImage = pygame.image.load('assets/player.png').convert_alpha()
        self.HIGHSCOREPATH = 'src/highscore.json'
        self.myBox = self.playerImage.get_rect()
        self.collisionGrid = [True, True, True, True]
        
        self.deltaTime = clock
        self.rect = self.playerImage.get_rect(center = (self.x, self.y))
        self.invincTimer = 0
        
        self.health = 100
        self.myHighScore = self.getHighscoreData()
        self.currentScore = 0

        self.invincMax = 200
        self.defInvincMax = 200
        self.damageMult = 5
        self.defDamageMult = 5
        self.getHighscoreData()
        
    def getHighscoreData(self, difficulty='easy'):
        file = open(self.HIGHSCOREPATH, 'r')
        highscore = json.load(file)
        
        return highscore.get(difficulty)
    
    def setHighscoreData(self):
        scores = {}
        file = open(self.HIGHSCOREPATH, 'r')
        scores = json.load(file)
        
        
        if self.myHighScore < self.currentScore:
            scores[self.myDifficulty] = self.currentScore
        
        
        file = open(self.HIGHSCOREPATH, 'w')
        json.dump(scores, file)
        
        
    def isColliding(self, rect, projectiles):
        collision = []
        if self.invincTimer == 0:
            for projectile in projectiles:
                if projectile.rect.contains(self.rect) and self.invincTimer == 0:
                    self.invincTimer = self.invincMax
                    self.health -= self.damageMult
                    break
        else:
            self.invincTimer -= 1 * self.deltaTime
            if self.invincTimer < 0:
                self.invincTimer = 0
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
    
        
        
    def handlePlayer(self, keys, rect, projectiles):
        self.collisionGrid = self.isColliding(rect, projectiles)
        if self.collisionGrid[2]:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.movePlayer('y', -1)
        if self.collisionGrid[3]:
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.movePlayer('y', 1)
        if self.collisionGrid[0]:
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.movePlayer('x', 1)
        if self.collisionGrid[1]:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.movePlayer('x', -1)
    
    def movePlayer(self, axis, sign):
        if axis == 'y':
            self.y += self.speed * self.deltaTime * sign
        else:
            self.x += self.speed * self.deltaTime * sign
        self.rect = self.playerImage.get_rect(topleft = (self.x, self.y))
    
    
    def renderPlayer(self, screen):
        if self.invincTimer == 0:
            screen.blit(self.playerImage, [self.x, self.y])
        else:    
            screen.blit(self.playerImage, [self.x, self.y])
        
    def difficultyStats(self, difficulty, name):
        if difficulty == 1:
            self.invincMax = self.defInvincMax
            self.damageMult = self.defDamageMult
        else:
            self.invincMax = self.defInvincMax - (difficulty * 55)
            self.damageMult = self.defDamageMult * difficulty
        self.myDifficulty = name[0][0].lower()
        self.myHighScore = self.getHighscoreData(self.myDifficulty)
        
        