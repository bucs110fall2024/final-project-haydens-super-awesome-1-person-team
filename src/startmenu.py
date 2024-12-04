import pygame
import pygame_menu
import pygame_menu.events

class StartMenu():
    def __init__(self):
        self.difficulty = 1
        
        
    def setDifficulty(self, _, value):
        self.difficulty = value
        
    def myFunc(self):
        print(self.difficulty)