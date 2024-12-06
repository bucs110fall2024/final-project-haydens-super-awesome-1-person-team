import pygame
import json

class Player():
    def __init__(self, xPos, yPos, clock):
        """
        Initializes the player object
        args:
            - xPos : int - starting x coordinate
            - yPos : int - starting y coordinate
            - clock : float - game's clock speed (used for some fps independent logic calculation)
        """
        self.playerState = 0
        self.speed = 0.35
        self.x = xPos
        self.y = yPos
        self.playerImage = pygame.image.load('assets/player.png').convert_alpha()
        self.HIGHSCOREPATH = 'src/highscore.json'
        self.myBox = self.playerImage.get_rect()
        self.collisionGrid = [True, True, True, True]
        
        self.deltaTime = clock
        self.rect = self.playerImage.get_rect(topleft = (self.x, self.y))
        self.invincTimer = 0
        
        self.health = 100
        self.myHighScore = self.getHighscoreData()
        self.currentScore = 30

        self.invincMax = 200
        self.defInvincMax = 200
        self.damageMult = 5
        self.defDamageMult = 5
        self.getHighscoreData()
        
        self.myDifficulty = 'easy'
        
    def getHighscoreData(self, difficulty='easy'):
        """
        Gets the highscore data from a JSON file
        args:
            - difficulty : string - the name of the difficulty, used as a key
        return: int - the high score with respect to the current difficulty from the JSON
        """
        file = open(self.HIGHSCOREPATH, 'r')
        highscore = json.load(file)
        
        return highscore.get(difficulty)
    
    def setHighscoreData(self):
        """
        Sets the highscore data from a JSON file
        args: none
        return: none
        """
        scores = {}
        file = open(self.HIGHSCOREPATH, 'r')
        scores = json.load(file)
        
        
        if self.myHighScore < self.currentScore:
            scores[self.myDifficulty] = self.currentScore
        
        
        file = open(self.HIGHSCOREPATH, 'w')
        json.dump(scores, file)
        
        
    def isColliding(self, rect, projectiles):
        """
        determines if the player is colliding with projectiles or the game's rectangle object
        args:
            - rect : pygame Rectangle - the rectangle that encapsulates the player
            - projectiles : list (Projectiles) - the projectile list that contains all current projectiles
        return: list (int) - the collision grid based on all conditions for possible collision
        """
        collision = []
        if self.invincTimer == 0:
            for projectile in projectiles:
                if projectile.hitbox.colliderect(self.rect) and self.invincTimer == 0:
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
        """
        determines if the player is colliding with projectiles or the game's rectangle object
        args:
            - rect : pygame Rectangle - the rectangle that encapsulates the player
            - projectiles : list (Projectiles) - the projectile list that contains all current projectiles
        return: list (int) - the collision grid based on all conditions for possible collision
        """                                                                                                                                                                                                         
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
        """
        moves the player
        args:
            - axis : string - the the axis that the player should be moved
            - sign: int - the direction that the player should be moved
        return: list (int) - the collision grid based on all conditions for possible collision
        """  
        if axis == 'y':
            self.y += self.speed * self.deltaTime * sign
        else:
            self.x += self.speed * self.deltaTime * sign
        self.rect = self.playerImage.get_rect(center = self.playerImage.get_rect(topleft = (self.x, self.y)).center).scale_by(0.5)
    
    
    def renderPlayer(self, screen):
        """
        draws the player
        args:
            - axis : string - the the axis that the player should be moved
            - sign: int - the direction that the player should be moved
        return: list (int) - the collision grid based on all conditions for possible collision
        """  
        if self.invincTimer == 0:
            screen.blit(self.playerImage, [self.x, self.y])
        else:    
            screen.blit(self.playerImage, [self.x, self.y])
            
        #pygame.draw.rect(screen, pygame.Color('#ffffff'), self.rect)
        
    def difficultyStats(self, difficulty, name):
        """
        handles difficulty stats that need to be updated when the difficulty is changed
        args:
            - difficulty : int - the difficulty (1-2-3) for (Easy-Medium-Hard)
            - name: tuple - tuple containing the difficulty name
        return: list (int) - the collision grid based on all conditions for possible collision
        """  
        if difficulty == 1:
            self.invincMax = self.defInvincMax
            self.damageMult = self.defDamageMult
        else:
            self.invincMax = self.defInvincMax - (difficulty * 55)
            self.damageMult = self.defDamageMult * difficulty
        self.myDifficulty = name[0][0].lower()
        self.myHighScore = self.getHighscoreData(self.myDifficulty)
        
        