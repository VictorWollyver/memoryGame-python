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
  BALL = pygame.image.load("assets/ball.gif")
  WIDTH_BALL = 640
  HEIGHT_BALL = 320

  def setDefaultConfigs(self):
    self.SCREEN.fill(self.BACKGROUND_COLOR)
    pygame.display.update()
    pygame.display.set_caption(self.APP_NAME)
    self.initGame()

  def initGame(self): 
    while self.RUNNING:
      for event in pygame.event.get():
        self.verifyIfCloseGame(event)
        rect = self.BALL.get_rect()
        speed = [2, 2]
        rect = rect.move(speed)
        if rect.left < 0 or rect.right > self.WIDTH_BALL:
          speed[0] = -speed[0]
        if rect.top < 0 or rect.bottom > self.HEIGHT_BALL:
          speed[1] = -speed[1]

        pygame.draw.rect(self.SCREEN, (255, 0, 0), rect, 1)
        self.SCREEN.blit(self.BALL, rect)
        pygame.display.update()
  
  def verifyIfCloseGame(self, event):
    if event.type == pygame.QUIT:
      self.RUNNING = False

newGame = memoryGame()
newGame.setDefaultConfigs()

