import pygame

class memoryGame:
  def __init__(self):
    self.screen_width = 900
    self.screen_height = 900
    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    self.running = True
    self.background_color = (255, 255, 255)

  def setDefaultConfigs(self):
    self.screen.fill(self.background_color)
    self.initGame()

  def initGame(self): 
    while self.running:
      for event in pygame.event.get():
        self.verifyIfCloseGame(event)
  
  def verifyIfCloseGame(self, event):
    if event.type == pygame.QUIT:
      self.running = False


if __name__ == "__main__":
  newGame = memoryGame()
  newGame.setDefaultConfigs()