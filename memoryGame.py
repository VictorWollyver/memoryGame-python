import pygame
from pygame.locals import*
from random import randint

class memoryGame():
  SCREEN_WIDTH = 900
  SCREEN_HEIGHT = 900
  SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  GAME = pygame.init()
  RUNNING = True
  BACKGROUND_COLOR = (255, 255, 255)
  FONTS_COLOR = (0,0,0)
  FONT = pygame.font.SysFont("Arial",50, True, True)
  
  def setDefaultConfigs(self):
    self.SCREEN.fill(self.BACKGROUND_COLOR)
    self.initGame()

  def initGame(self): 
    while self.RUNNING:
      for event in pygame.event.get():
        self.verifyIfCloseGame(event)
        self._draw_menu()
        print(event)
  
  def verifyIfCloseGame(self, event):
    if event.type == pygame.QUIT:
      self.RUNNING = False

  def _draw_menu(self):
    memoryGame.SCREEN.fill(memoryGame.BACKGROUND_COLOR)
    self.title= memoryGame.FONT.render("Bem vindo ao Memory.py", True, memoryGame.FONTS_COLOR)
    self.start=memoryGame.FONT.render("Click em [E]nter para começar.", True, memoryGame.FONTS_COLOR)
    memoryGame.SCREEN.blit(self.title,(memoryGame.SCREEN_WIDTH//2 - self.title.get_width()// 2, memoryGame.SCREEN_HEIGHT//4))
    memoryGame.SCREEN.blit(self.start,(memoryGame.SCREEN_WIDTH//2 - self.start.get_width()// 2,memoryGame.SCREEN_HEIGHT//2))
    pygame.display.flip()



newGame = memoryGame()
newGame.setDefaultConfigs()


# self.font_m = font_menu(pygame.font.SysFont("comandi", 30, True, True))