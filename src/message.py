import pygame

class Message():
    def __init__(self):
        """
        Initializes the Message object
        args:
            none
        """
        self.messageList = {
            0: ["It's Malo! He's a proboscis", "monkey!"],
            2: ["Word around town is that", "he doesen't really like you.."],
            4: ["You get the sense you are", "going to find out why this game", "is called MALO's WRATH"],
            6: ["Well then, you have a project", "to grade, and he has his wrath", "to unleash on you"],
            8: ["Let's get this over with.."]
            
        }
        self.font = pygame.font.Font('assets/fight-mono.ttf', 24)
           
    def handleMessageSeq(self, state):
        """
        Handles drawing of the dialogue
        args:
            - state : int - the current game state / dialogue state
        return: int - the new state of the game / dialogue
        """
        if state < 8 and state % 2 == 0:
            return state + 2
        else:
            return state + 1
        
    def showMessage(self, state, screen, rect):
        """
        Handles drawing of the dialogue
        args:
            - state : int - the current game state / dialogue state
            - screen : pygame Surface object - the whole game screen
            - rect : pygame Rectangle object - the bounding rectangle
        return: none
        """
        currentLines = self.messageList[state]
        for i in range(len(currentLines)):
            text = self.font.render(currentLines[i], True, pygame.Color("#ffffff"))
            screen.blit(text, rect.move(0, (40 * i)))
        