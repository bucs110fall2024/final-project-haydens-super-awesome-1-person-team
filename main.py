import pygame
from src.controller import Controller

def main():
    pygame.init()
    myController = Controller()
    myController.mainloop()
    

# https://codefather.tech/blog/if-name-main-python/
if __name__ == '__main__':
    main()
