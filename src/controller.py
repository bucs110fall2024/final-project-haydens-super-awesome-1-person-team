import pygame
import pygame_menu
import pygame_menu.themes
import pygame_menu.widgets
import pygame_menu.widgets.selection
import pygame_menu.widgets.selection.right_arrow
import pygame_menu.widgets.widget
from src.player import Player
from src.rectangle import Rectangle
from src.malo import Malo
from src.message import Message
from src.gui import Gui


class Controller:
  
  def __init__(self):
    pygame.init()
    pygame.display.set_caption('MALOS WRATH')
    self.events = pygame.event.get()
    self.screen = pygame.display.set_mode([640, 480])
    self.difficulty = 1
    self.state = "STARTMENU"
    self.keys = pygame.key.get_pressed()
    
    self.clock = pygame.time.Clock()
    self.fps = self.clock.tick(60)
    
    
    self.rectangle = Rectangle()
    self.malo = Malo(220, 10, 200, self.fps)
    self.message = Message()
    self.gui = Gui()
    self.isRunning = True
    
    
    self.player = Player(300, 350, self.fps)
    
    self.gamestate = 0
    
    
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
    while self.isRunning:
      if self.state == "STARTMENU":
        self.menuloop()
      elif self.state == "WRATH":
        self.gameloop()
      if self.state == "GAMEOVER":
        self.gameoverloop()
      
  def setDifficulty(self, name, value):
    self.difficulty = value
    self.player.difficultyStats(self.difficulty, name)
    self.malo.difficultyStats(self.difficulty)
    self.gui.difficultyName(name)
      
      
  
  ### below are some sample loop states ###

  def menuloop(self):
      while self.state == "STARTMENU":
        if self.menu.is_enabled():
          self.menu.update(pygame.event.get())
          self.menu.draw(self.screen)
          
          
        pygame.display.update()
          
      
      
      
      #event loop

      #update data

      #redraw
      
  def gameloop(self):
        
        
        self.clock.tick(60)
        
        self.screen.fill("#000000")
        
        
        
        
        self.malo.renderMalo(self.screen)
        
        
        if (self.gamestate == 0) or (self.gamestate % 2 == 0):
          self.message.showMessage(self.gamestate, self.screen, self.rectangle.getMessageRect())
        else:
          if self.rectangle.mode == 0:
            self.rectangle.changeSize(-2)
          self.player.renderPlayer(self.screen)
          self.player.handlePlayer(pygame.key.get_pressed(), self.rectangle.rect, self.malo.projectiles)
          self.malo.handleAttacks(self.screen, self.player)
          
          
          
          
          
        
        self.rectangle.renderRectangle(self.screen)
        
        self.gui.renderGUI(self.screen, self.player.health, self.malo.round, self.player.myHighScore, self.player.currentScore)
        
        
        
        for events in pygame.event.get():
          if events.type == pygame.QUIT:
            self.isRunning = False
          
          if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_RETURN and self.gamestate % 2 == 0:
              self.gamestate = self.message.handleMessageSeq(self.gamestate)
            if events.key == pygame.K_ESCAPE:
              self.player.health = 0
              
        if self.player.health <= 0:
          self.player.setHighscoreData()
          self.state = 'GAMEOVER'
            
              
        
        
        
      
        pygame.display.update()
      #event loop

      #update data

      #redraw
    
  def gameoverloop(self):
    
    self.clock.tick(60)
    self.screen.fill("#000000")
    self.malo.renderMalo(self.screen)
    
    
    self.gui.renderGameOver(self.screen, self.player.currentScore, self.player.myHighScore)
    
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
          self.isRunning = False
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_RETURN:
              self.__init__()
            
    pygame.display.update()
      #event loop

      #update data

      #redraw
      
  def start_wrath(self):
    self.state = "WRATH"
