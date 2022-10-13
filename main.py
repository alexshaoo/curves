import pygame
import math
import numpy as np

# constants
WHITE = (235, 235, 235)
BLACK = (20, 20, 20)
RED = (242, 2, 2)
GREEN = (2, 242, 102)
BLUE = (2, 146, 242)
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
count = 0

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