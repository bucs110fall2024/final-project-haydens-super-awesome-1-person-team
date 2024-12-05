import pygame


class Gui():
    def __init__(self):
        """
        Initializes the GUI object
        args:
            none
        """
        self.healthDim = [270, 430, 100, 40]
        self.healthB = pygame.Rect(self.healthDim)
        self.healthF = pygame.Rect(self.healthDim)
        
        
        self.font = pygame.font.Font('assets/fight-mono.ttf', 30)
        self.font2 = pygame.font.Font('assets/fight-mono.ttf', 60)
        self.font3 = pygame.font.Font('assets/fight-mono.ttf', 20)
        self.white = pygame.Color('#ffffff')
        
        self.hp = self.font.render("HP", True, self.white)
        self.total = self.font.render("/100", True, self.white)
        self.current = self.font.render("100", True, self.white)
        
        self.gameover = self.font2.render("GAME OVER!", True, self.white)
        self.gameoverMsg1 = self.font.render("You tried on EASY difficulty!", True, self.white)
        self.gameoverMsg2 = self.font.render("Your score was: ", True, self.white)
        self.gameoverMsg3 = self.font.render("Your high score is: ", True, self.white)
        
        self.gameoverRect = self.gameover.get_rect(center = (640/2, 480/2))
        self.gameoverMsg1Rect = self.gameoverMsg1.get_rect(center = (640/2, 300))
        self.gameoverMsg2Rect = self.gameoverMsg2.get_rect(center = (640/2, 340))
        self.gameoverMsg3Rect = self.gameoverMsg3.get_rect(center = (640/2, 380))
        
        
        self.currentRound = self.font3.render("ROUND:", True, self.white)
        self.bestScore = self.font3.render("BEST:", True, self.white)
        self.currentScore = self.font3.render("CURRENT:", True, self.white)
        
        self.difficulty = 'EASY'
        
    def difficultyName(self, difficulty):
        """
        Stores the name of whatever the difficulty mode is on for the game for the game over message.
        args:
            - difficulty : tuple - passed by the start menu function whenever the difficulty mode is changed. 
        returns: none
        """
        
        self.difficulty = difficulty[0][0].upper()
        combinedStr = "You tried on " + self.difficulty + " difficulty!"   
        self.gameoverMsg1 = self.font.render(combinedStr, True, self.white)
        self.gameoverMsg1Rect = self.gameoverMsg1.get_rect(center = (640/2, 300))

    
    def renderGUI(self, screen, health, round, bestScore, currentScore):
        """
        Renders the GUI and any relevant information.
        args:
            - screen : pygame Surface object - the whole game screen
            - health : int - the player's current health
            - round : int - Malo's current attack round
            - bestScore : int - the player's current high score with respect to the game difficulty
            - currentScore : int - the player's current score
        returns: none     
        """
        
        self.current = self.font.render(str(health), True, self.white)
        self.currentRound = self.font3.render(f"ROUND: {round}", True, self.white)
        if currentScore > bestScore:
            self.bestScore = self.font3.render(f"BEST: {currentScore}", True, self.white)
        else:
            self.bestScore = self.font3.render(f"BEST: {bestScore}", True, self.white)
        self.currentScore = self.font3.render(f"CURRENT: {currentScore}", True, self.white)
        
        self.healthDim[2] = health
        screen.blit(self.hp, [230, 430])
        screen.blit(self.total, [450, 430])
        screen.blit(self.current, [385, 430])
        pygame.draw.rect(screen, pygame.Color("#ff0000"), self.healthB)
        pygame.draw.rect(screen, pygame.Color("#ffff00"), pygame.Rect(self.healthDim))
        screen.blit(self.currentRound, [0, 0])
        screen.blit(self.currentScore, [0, 30])
        screen.blit(self.bestScore, [0, 60])
        
        
    def renderGameOver(self, screen, currentScore, bestScore):
        """
        Renders the game over screen.
        args:
            - screen : pygame Surface object - the whole game screen
            - bestScore : int - the player's current high score with respect to the game difficulty
            - currentScore : int - the player's current score
        returns: none     
        """
        
        self.gameoverMsg2 = self.font.render(f"Your score was: {currentScore}", True, self.white)
        if currentScore > bestScore:
            self.gameoverMsg3 = self.font.render(f"Your high score is: {currentScore}", True, self.white)
        else:
            self.gameoverMsg3 = self.font.render(f"Your high score is: {bestScore}", True, self.white)
            
        self.gameoverMsg2Rect = self.gameoverMsg2.get_rect(center = (640/2, 340))
        self.gameoverMsg3Rect = self.gameoverMsg3.get_rect(center = (640/2, 380))
        
        
        
        screen.blit(self.gameover, self.gameoverRect)
        screen.blit(self.gameoverMsg1, self.gameoverMsg1Rect)
        screen.blit(self.gameoverMsg2, self.gameoverMsg2Rect)
        screen.blit(self.gameoverMsg3, self.gameoverMsg3Rect)