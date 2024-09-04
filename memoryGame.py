import pygame
from pygame.locals import *

class memoryGame:
  SCREEN_WIDTH = 900
  SCREEN_HEIGHT = 900
  SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  GAME = pygame.init()
  RUNNING = True
  BACKGROUND_COLOR = (255, 255, 255)
  APP_NAME = "Memory.Py"

  def setDefaultConfigs(self):
    self.SCREEN.fill(self.BACKGROUND_COLOR)
    pygame.display.update()
    pygame.display.set_caption(self.APP_NAME)
    self.initGame()

  def initGame(self): 
    while self.RUNNING:
      for event in pygame.event.get():
        self.verifyIfCloseGame(event)
        print(event)
  
  def verifyIfCloseGame(self, event):
    if event.type == pygame.QUIT:
      self.RUNNING = False

newGame = memoryGame()
newGame.setDefaultConfigs()

