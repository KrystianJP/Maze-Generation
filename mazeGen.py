import random, time, pygame, sys

sys.setrecursionlimit(10**6)

pygame.init()
screen = pygame.display.set_mode((800,800))

# *** global maze gen variables ***
allNodes = []
unvisited = []
path = []

x = 40
last = x**2 - 1

# colours
white = (255,255,255)
blue = (145, 163, 176)
red = (203,65,84)
black = (0,0,0)

# *** global GUI variables ***
generating = True
clock = pygame.time.Clock()
fps = 30


class Node:
  size = 800 / x

  def __init__(self, nr):
    self.nr = nr

    self.position = (Node.size * (nr % x), Node.size * (nr // x))

  
  # going to next unvisited node
  def next(self):
    neighbourNodes = self.findNeighbours(self.nr)

    if self in unvisited: # don't do if it had been backtracked to
      unvisited.remove(self)
      path.append(self)

    self.draw()

    if not neighbourNodes:
      self.backtrack()
      return

    chosenNeighbour = self.chooseNeighbour(neighbourNodes)

    # removing the walls
    wall = self.whichWall(chosenNeighbour)
    for node in [self, chosenNeighbour]:
      if wall == "left":
        allNodes[self.nr].left = False
        allNodes[chosenNeighbour.nr].right = False
      elif wall == "right":
        allNodes[self.nr].right = False
        allNodes[chosenNeighbour.nr].left = False
      elif wall == "top":
        allNodes[self.nr].top = False
        allNodes[chosenNeighbour.nr].bottom = False
      elif wall == "bottom":
        allNodes[self.nr].bottom = False
        allNodes[chosenNeighbour.nr].top = False


    chosenNeighbour.next()
  
  def backtrack(self): # does .next() to the node before
    if not unvisited:
      self.finished()
      return
    path.remove(self)
    path[-1].next()
    

  def findNeighbours(self, nr): # finds a node's neighbours depending on its number
    neighbours = []
    nodeNeighbours = []

    # possible adjacent neighbours, accounting for bounds
    if nr % x != 0:
      neighbours.append(nr-1)
    if nr % x != (x-1):
      neighbours.append(nr+1)
    if last-nr >= x:
      neighbours.append(nr+x)
    if nr - x >= 0:
      neighbours.append(nr-x)


    # turning those numbers into nodes
    for node in unvisited:
      if node.nr in neighbours:
        nodeNeighbours.append(node)
        
    return nodeNeighbours

  def chooseNeighbour(self, neighbours):
    index = random.randint(0, len(neighbours)-1)
    return neighbours[index]

  def whichWall(self, node):
    wall = ""
    if node.nr - self.nr == x:
      wall = "bottom"
    elif node.nr - self.nr == -x:
      wall = "top"
    elif node.nr - self.nr == -1:
      wall = "left"
    elif node.nr - self.nr == 1:
      wall = "right"

    return wall


  @staticmethod
  def draw():
    for node in allNodes:
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
  def finished():
    global generating
    generating = False

for nr in range(x**2):
  unvisited.append(Node(nr))
  allNodes.append(Node(nr))

# setting GUI variables on GUI version of nodes
for node in allNodes:
  node.background = blue
  node.left = True
  node.right = True
  node.top = True
  node.bottom = True


while True:
  clock.tick(fps)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
  if generating:
    unvisited[0].next()
  pygame.display.update()





