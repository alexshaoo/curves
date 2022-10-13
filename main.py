import pygame
import math
import numpy as np

# constants
WHITE = (235, 235, 235)
BLACK = (20, 20, 20)
RED = (242, 2, 2)
GREEN = (2, 242, 102)
BLUE = (2, 146, 242)
MARGIN = 5
STEP = 0.01
WIDTH, HEIGHT = 1280, 720
DIMENSIONS = (WIDTH, HEIGHT)
FPS = 165

pygame.init()
screen = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption("Curves")
screen.fill(WHITE)
clock = pygame.time.Clock()

class button():
  def __init__(self, color, x, y, width, height, text=''):
    self.color = color
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.text = text

  def draw(self, win, outline=None):
    if outline:
      pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

    pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

    if self.text != '':
      font = pygame.font.SysFont('comicsans', 30)
      text = font.render(self.text, 1, (0, 0, 0))
      win.blit(text, 
      (self.x + (self.width / 2 - text.get_width() / 2), 
      self.y + (self.height / 2 - text.get_height() / 2)))

  def isOver(self, pos):
    if pos[0] > self.x and pos[0] < self.x + self.width:
      if pos[1] > self.y and pos[1] < self.y + self.height:
        return True
    return False

points = []
knots = []

def redraw():
  screen.fill(WHITE)
  l = len(points)
  for i in range(l-1):
    pygame.draw.line(screen, GREEN, points[i], points[i+1], 2)
  for i in range(l):
    pygame.draw.rect(screen, BLUE, (points[i][0]-MARGIN, points[i][1]-MARGIN, 2*MARGIN, 2*MARGIN), 5)

def bezier():
  redraw()
  l = len(points)
  for i in np.arange(0, 1, STEP):
    z = np.zeroes(2)
    for j in range(l):
      z += np.dot((math.factorial(l-1) / (math.factorial(j) * math.factorial(l-j-1))) * (1-i)**(l-j-1) * i**j, points[j])
    pygame.draw.circle(screen, RED, (int(z[0]), int(z[1])), 3)



run = True
pressed = 0
old_pressed = 0
old_left_click = 0
old_right_click = 0

selected = -1
bezier_button = button((0,255,0),650,200,120,70,"Bezier")

while run:
  clock.tick(FPS)
  frameRate = int(clock.get_fps())
  pygame.display.set_caption("Bezier Curve")

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        run = False

    pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
      pressed = -1
      bezier()
    elif event.type == pygame.MOUSEBUTTONUP:
      pressed = 1
    else:
      pressed = 0



  pygame.display.update()
pygame.quit()