import pygame
import math
import numpy as np

pygame.init()

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
FPS = 60
FONT = pygame.font.Font("freesansbold.ttf", 22)
CURVES = ["lagrange", "bezier", "hermite_cubic", "cubic_spline"]

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
      pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
    pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

    if self.text != '':
      text = FONT.render(self.text, 1, (0, 0, 0))
      win.blit(text, 
      (self.x + (self.width/2 - text.get_width()/2), 
      self.y + (self.height/2 - text.get_height()/2)))

  def clicked(self, pos):
    return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

points = []
knots = []

def redraw():
  screen.fill(WHITE)
  l = len(points)
  for i in range(l-1):
    pygame.draw.line(screen, GREEN, points[i], points[i+1], 2)
  for i in range(l):
    pygame.draw.rect(screen, BLUE, (points[i][0]-MARGIN, points[i][1]-MARGIN, 2*MARGIN, 2*MARGIN), 5)

  lagrange_button.draw(screen, (0, 0, 0))
  bezier_button.draw(screen, (0, 0, 0))
  hermite_cubic_button.draw(screen, (0, 0, 0))
  cubic_spline_button.draw(screen, (0, 0, 0))

  if abs(selected_button) == 1:
    curve_type = "Curve Type: Lagrange"
  elif abs(selected_button) == 2:
    curve_type = "Curve Type: Bezier"
  elif abs(selected_button) == 3:
    curve_type = "Curve Type: Hermite Cubic"
  elif abs(selected_button) == 4:
    curve_type = "Curve Type: Cubic Spline"
  else:
    curve_type = "Curve Type: None"
  curve_text = FONT.render(curve_type, True, BLACK)
  screen.blit(curve_text, (10, 10))

def lagrange():
  pass

def bezier():
  redraw()
  l = len(points)
  for i in np.arange(0, 1, STEP):
    z = np.zeroes(2)
    for j in range(l):
      z += np.dot((math.factorial(l-1) / (math.factorial(j) * math.factorial(l-j-1))) * (1-i)**(l-j-1) * i**j, points[j])
    pygame.draw.circle(screen, RED, (int(z[0]), int(z[1])), 3)

def hermite_cubic():
  pass

def cubic_spline():
  pass

def draw_curve(color=GREEN, thickness=2):
  l = len(points)
  if l < 2:
    return
  for i in range(l-1):
    pygame.draw.line(screen, color, points[i], points[i+1], thickness)
  for i in range(l):
    pygame.draw.rect(screen, BLUE, (points[i][0]-MARGIN, points[i][1]-MARGIN, 2*MARGIN, 2*MARGIN), 5)
    if l > 2:
      if selected_button == 1:
        lagrange()
      elif selected_button == 2:
        bezier()
      elif selected_button == 3:
        hermite_cubic()
      elif selected_button == 4:
        cubic_spline()
      else:
        pass

run = True
pressed = 0
old_pressed = 0
old_left_click = 0
old_right_click = 0

selected = -1
selected_button = -1

lagrange_button, bezier_button, hermite_cubic_button, cubic_spline_button = [button(BLACK, 650, 100*i, 100, 30, CURVES[i]) for i in range(4)]

while run:
  time_passed = clock.tick(FPS)
  # frameRate = int(clock.get_fps())

  lagrange_button.draw(screen, (0, 0, 0))
  bezier_button.draw(screen, (0, 0, 0))
  hermite_cubic_button.draw(screen, (0, 0, 0))
  cubic_spline_button.draw(screen, (0, 0, 0))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        run = False

    pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
      l = len(points)
      pressed = -1
      if l > 2:
        if lagrange_button.clicked(pos):
          selected_button = 1
          lagrange()
        elif bezier_button.clicked(pos):
          selected_button = 2
          bezier()
        elif hermite_cubic_button.clicked(pos):
          selected_button = 3
          hermite_cubic()
        elif cubic_spline_button.clicked(pos):
          selected_button = 4
          cubic_spline()
        else:
          selected_button = -1
    elif event.type == pygame.MOUSEBUTTONUP:
      pressed = 1
    else:
      pressed = 0

  left_click, _, right_click = pygame.mouse.get_pressed()
  x, y = pygame.mouse.get_pos()

  # click
  if pressed and not old_pressed and not left_click and old_left_click:
    points.append([x,y])
    pygame.draw.rect(screen, BLUE, (x-MARGIN, y-MARGIN, 2*MARGIN, 2*MARGIN), 5)
  # drag
  elif not pressed and not old_pressed and left_click and old_left_click:
    for i, point in enumerate(points):
      if math.isclose(x, point[0], rel_tol=0.1) and math.isclose(y, point[1], rel_tol=0.1):
        selected = i
        break
  # hold while moving
  elif pressed and not old_pressed and left_click and not old_left_click:
    if selected != -1:
      screen.fill(WHITE)
      points[selected] = [x, y]
  # release
  elif pressed and old_pressed and not left_click and not old_left_click:
    selected = -1
  # right click
  elif pressed and not old_pressed and not right_click and old_right_click:
    for i, point in enumerate(points):
      if math.isclose(x, point[0], rel_tol=0.1) and math.isclose(y, point[1], rel_tol=0.1):
        points.pop(i)
        screen.fill(WHITE)
        break
  
  if len(points) > 1:
    draw_curve()

  pygame.display.update()
  old_pressed = pressed
  old_left_click = left_click
  old_right_click = right_click
  
pygame.quit()