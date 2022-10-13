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

  pygame.display.update()
pygame.quit()