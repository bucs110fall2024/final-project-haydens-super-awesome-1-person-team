import pygame

class Rectangle():
    
    def __init__(self, clock):
        """
        Initializes the rectangle object
        args:
            - clock : float - game's clock speed (used for some fps independent logic calculation)
        """
        self.rectState = 0
        self.messageDim = [70, 220, 500, 200]
        self.timer = 100
        self.mode = 0
        self.rect = pygame.Rect(self.messageDim)
        self.deltaTime = clock
    
    def changeSize(self, factor):
        """
        animates changing the size of the rectangle
        args:
            - factor : int - the scalar multiple for the rectangle animation
        return: none
        """  
        if self.timer > 0:
            self.rect.inflate_ip(factor, 0)
            self.timer -= 1 * self.deltaTime
        else:
            self.mode = 1
            self.timer = 5
        
    
    def getMessageRect(self):
        """
        gets the rectangle that is used for the message object
        args: none
        return: pygame Rectangle - the message box
        """  
        padRect = [0, 0, 0, 0]
        for i in range(len(self.messageDim)):
            padRect[i] = self.messageDim[i] + 20
        
        return pygame.Rect(padRect)
    
    
    def renderRectangle(self, screen):
        """
        handles drawing the rectangle
        args:
            - screen : pygame Surface object - the whole game screen
        return: none
        """  
        pygame.draw.rect(screen, pygame.Color("#ffffff"), self.rect, 3) 
        