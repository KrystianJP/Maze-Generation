import random, time, pygame, sys

sys.setrecursionlimit(10**6)

pygame.init()
screen = pygame.display.set_mode((800,800))

# colours
white = (255,255,255)
blue = (145, 163, 176)
red = (203,65,84)
black = (0,0,0)

# *** global GUI variables ***
generating = True
clock = pygame.time.Clock()
fps = 60

x = int(input("Grid size: "))

'''
IN ORDER TO USE: YOU MUST USE THIS SKELETON:

Node.mazeGeneration(10, 800, (0,0))

current = Node.unvisited[0]

while True:
  clock.tick(fps)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
  
  keys = pygame.key.get_pressed()
  if not Node.generating:
    if keys[pygame.K_SPACE]:
      Node.pathDraw()

  if Node.generating:
    current = current.next()
  pygame.display.update()
'''


class Node:
  allNodes = []
  unvisited = []
  path = []
  finalPath = []
  generating = True

  def __init__(self, nr):
    self.nr = nr

    self.position = ((Node.size * (nr % Node.x) + Node.mazePosition[0]), (Node.size * (nr // Node.x)+Node.mazePosition[1]))

  
  # going to next unvisited node
  def next(self):

    neighbourNodes = self.findNeighbours(self.nr)

    if self in Node.unvisited: # don't do if it had been backtracked to
      Node.unvisited.remove(self)
      Node.path.append(self)

      if self.nr == Node.last: # saving the path to the end
        Node.finalPath = Node.path[:]

    self.draw()

    if not neighbourNodes:
      return self.backtrack()

    chosenNeighbour = self.chooseNeighbour(neighbourNodes)

    # removing the walls
    wall = self.whichWall(chosenNeighbour)
    for node in [self, chosenNeighbour]:
      if wall == "left":
        Node.allNodes[self.nr].left = False
        Node.allNodes[chosenNeighbour.nr].right = False
      elif wall == "right":
        Node.allNodes[self.nr].right = False
        Node.allNodes[chosenNeighbour.nr].left = False
      elif wall == "top":
        Node.allNodes[self.nr].top = False
        Node.allNodes[chosenNeighbour.nr].bottom = False
      elif wall == "bottom":
        Node.allNodes[self.nr].bottom = False
        Node.allNodes[chosenNeighbour.nr].top = False

    return chosenNeighbour
  
  def backtrack(self): # does .next() to the node before
    if not Node.unvisited:
      self.finished()
      return
    Node.path.remove(self)
    return Node.path[-1].next()
    

  def findNeighbours(self, nr): # finds a node's neighbours depending on its number
    neighbours = []
    nodeNeighbours = []

    # possible adjacent neighbours, accounting for bounds
    if nr % Node.x != 0:
      neighbours.append(nr-1)
    if nr % Node.x != (Node.x-1):
      neighbours.append(nr+1)
    if Node.last-nr >= Node.x:
      neighbours.append(nr+Node.x)
    if nr - Node.x >= 0:
      neighbours.append(nr-Node.x)


    # turning those numbers into nodes
    for node in Node.unvisited:
      if node.nr in neighbours:
        nodeNeighbours.append(node)
        
    return nodeNeighbours

  def chooseNeighbour(self, neighbours):
    index = random.randint(0, len(neighbours)-1)
    return neighbours[index]

  def whichWall(self, node):
    wall = ""
    if node.nr - self.nr == Node.x:
      wall = "bottom"
    elif node.nr - self.nr == -(Node.x):
      wall = "top"
    elif node.nr - self.nr == -1:
      wall = "left"
    elif node.nr - self.nr == 1:
      wall = "right"

    return wall


  @staticmethod
  def draw():
    for node in Node.allNodes:
      # draw each rectangle
      pygame.draw.rect(screen, node.background, (node.position[0], node.position[1], Node.size, Node.size))

      # drawing each wall if it exists
      if node.left:
        pygame.draw.line(screen, black, node.position, (node.position[0], node.position[1] + Node.size))
      if node.right:
        pygame.draw.line(screen, black, (node.position[0] + Node.size, node.position[1]), (node.position[0] + Node.size, node.position[1] + Node.size))
      if node.top:
        pygame.draw.line(screen, black, node.position, (node.position[0] + Node.size, node.position[1]))
      if node.bottom:
        pygame.draw.line(screen, black, (node.position[0], node.position[1] + Node.size), (node.position[0] + Node.size, node.position[1] + Node.size))

  @staticmethod
  def pathDraw():  # draws the path from 0 to last
    for node in Node.finalPath:
      Node.allNodes[node.nr].background = red
    Node.draw()


  @staticmethod
  def finished():  # will need to change to reuse
    Node.generating = False

  @classmethod
  def mazeGeneration(cls, xNodes, mazeSize=800, position=(0,0)):  # creating the maze depending on grid size
    cls.x = xNodes
    cls.last = xNodes**2 - 1
    cls.size = int(mazeSize/ Node.x)
    cls.mazePosition = position
    for nr in range(xNodes**2):
      Node.unvisited.append(Node(nr))
      Node.allNodes.append(Node(nr))

    # setting GUI variables on GUI version of nodes
    for node in Node.allNodes:
      node.background = blue
      node.left = True
      node.right = True
      node.top = True
      node.bottom = True




Node.mazeGeneration(x, 800, (0,0))

current = Node.unvisited[0]

while True:
  clock.tick(fps)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
  
  keys = pygame.key.get_pressed()
  if not Node.generating:
    if keys[pygame.K_SPACE]:
      Node.pathDraw()

  if Node.generating:
    current = current.next()
  pygame.display.update()
