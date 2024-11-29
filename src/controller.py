import pygame
import pygame_menu
import pygame_menu.themes
import pygame_menu.widgets
import pygame_menu.widgets.selection
import pygame_menu.widgets.selection.right_arrow
import pygame_menu.widgets.widget
import pyganim
from src.player import Player
from src.rectangle import Rectangle
from src.malo import Malo
from src.message import Message
from src.gui import Gui
from src.fruits import Fruits
import random


class Controller:
  
  def __init__(self):
    pygame.init()
    pygame.display.set_caption('MALOS WRATH')
    self.events = pygame.event.get()
    self.screen = pygame.display.set_mode([640, 480])
    self.difficulty = 1
    self.state = "STARTMENU"
    self.keys = pygame.key.get_pressed()
    
    self.player = Player(300, 350)
    self.rectangle = Rectangle()
    self.malo = Malo(220, 10, 200)
    self.message = Message()
    self.gui = Gui()
    
    self.gamestate = 0
    self.projectiles = []
    
    
    self.menu = self.setupSM()
    
  
  def setupSM(self):
    
    startMenuTheme = pygame_menu.themes.Theme()
    startMenuTheme.background_color = pygame.Color("#e07f36")
    startMenuTheme.title_background_color = pygame.Color("#b44924")
    startMenuTheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
    startMenuTheme.title_font = pygame_menu.font.FONT_8BIT
    startMenuTheme.title_font_shadow = True
    startMenuTheme.widget_font_shadow = True
    startMenuTheme.widget_font = pygame_menu.font.FONT_MUNRO
    startMenuTheme.widget_padding = 40
    
    
    
    startMenu = pygame_menu.Menu('MALOS WRATH', 600, 400, theme=startMenuTheme)
    
    startMenu.add.button("Play", self.start_wrath)
    startMenu.add.selector("Difficulty", [("Easy", 1), ("Medium", 2), ("Hard", 3)], onchange=self.setDifficulty)
    
    return startMenu
    
  def mainloop(self):
    while True:
      if self.state == "STARTMENU":
        self.menuloop()
      elif self.state == "WRATH":
        self.gameloop()
        
      print("Bruh")
      
  def setDifficulty(self, _, value):
    self.difficulty = value
      
      
  
  ### below are some sample loop states ###

  def menuloop(self):
      while self.state == "STARTMENU":
        if self.menu.is_enabled():
          self.menu.update(pygame.event.get())
          self.menu.draw(self.screen)
          
          
        print("Im still going!")  
        pygame.display.update()
          
      
      
      
      #event loop

      #update data

      #redraw
      
  def gameloop(self):
      while self.state == "WRATH":
        
        
          
        
        self.screen.fill("#000000")
        
        
        
        
        self.malo.renderMalo(self.screen)
        
        if (self.gamestate == 0) or (self.gamestate % 2 == 0):
          self.message.showMessage(self.gamestate, self.screen, self.rectangle.getMessageRect())
        else:
          if self.rectangle.mode == 0:
            self.rectangle.changeSize(-2)
          self.player.renderPlayer(self.screen)
          self.player.handlePlayer(pygame.key.get_pressed(), self.rectangle.rect)
          
          
          timer = pygame.time.get_ticks()
          if timer - self.malo.lastProjSpawn > self.malo.projInterval:
            self.malo.lastProjSpawn = timer
            print("FIre!")
            for i in range(5):
              self.projectiles.append(Fruits(108 + (108 * i), 100, random.randint(0, 4)))
            print(f"Projectile spawned! Total projectiles: {len(self.projectiles)}")
          
          for i in self.projectiles:
            i.fruitRender(self.screen, self.player.x, self.player.y)
            if i.y > 600:
              self.projectiles.remove(i)
          
          
        
        self.rectangle.renderRectangle(self.screen)
        #print("HI")
        
        self.gui.renderHealth(self.screen, self.player.health)
        
        
        
        for events in pygame.event.get():
          if events.type == pygame.QUIT:
            pygame.quit()
          
          if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_RETURN and self.gamestate % 2 == 0:
              self.gamestate = self.message.handleMessageSeq(self.gamestate)
            
            if events.key == pygame.K_ESCAPE:
              self.state = "STARTMENU"
              
        
        
        
        
        #print("Now im running!")
        pygame.display.update()
      #event loop

      #update data

      #redraw
    
  def gameoverloop(self):
      pass
      #event loop

      #update data

      #redraw
      
  def start_wrath(self):
    print("I got ran!")
    self.state = "WRATH"
