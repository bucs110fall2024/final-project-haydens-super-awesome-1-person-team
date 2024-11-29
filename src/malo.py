import pygame
import pyganim

class Malo():
    def __init__(self, xPos, yPos, scale):
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
        
        self.lastProjSpawn = 0
        self.projInterval = 6000
        
        self.parts = {}
        for part, path in self.partPaths.items():
            original_image = pygame.image.load(path).convert_alpha() 
            scaled_image = pygame.transform.scale(original_image, (self.size, self.size))
            self.parts[part] = scaled_image
        
        self.x = xPos
        self.y = yPos
        
        
        
        
        

        
    def renderMalo(self, screen):
        for part, image in self.parts.items(): 
            screen.blit(image, [self.x, self.y])
    
    def intro(self):
        pass
    