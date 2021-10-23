import random, time, pygame, sys

sys.setrecursionlimit(10**6)

pygame.init()
screen = pygame.display.set_mode((800,800))

# *** global maze gen variables ***
allNodes = []
unvisited = []
path = []

x = 20
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

wallOpposites = {
  "left":"right",
  "right":"left",
  "top":"bottom",
  "bottom":"top"
}


class Node:
  size = 800 / x

  def __init__(self, nr):
    self.nr = nr

    self.position = (Node.size * (nr % x), Node.size * (nr // x))

    self.left,self.right,self.top,self.bottom = True
  
  # going to next unvisited node
  def next(self):
    neighbourNodes = self.findNeighbours(self.nr)

    if self in unvisited: # don't do if it had been backtracked to
      unvisited.remove(self)
      path.append(self)

    if self in path:
      allNodes[self.nr].background = red

    self.draw()

    if not neighbourNodes:
      self.backtrack()
      return

    chosenNeighbour = self.chooseNeighbour(neighbourNodes)



    chosenNeighbour.next()
  
  def backtrack(self): # does .next() to the node before
    if not unvisited:
      self.finished()
      return
    allNodes[self.nr].background = blue
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

  @staticmethod
  def draw():
    for node in allNodes:
      pygame.draw.rect(screen, node.background, (node.position[0], node.position[1], Node.size, Node.size))

      if node.left:
        pygame.draw.line(screen, black, node.position, (node.position[0], node.position[1] + size))


  @staticmethod
  def finished():
    global generating
    print("FINAL PATH")
    nodenrs = []
    for node in path:
      nodenrs.append(node.nr)
    print(nodenrs)
    generating = False

for nr in range(x**2):
  unvisited.append(Node(nr))
  allNodes.append(Node(nr))

for node in allNodes:
  node.background = black


while True:
  clock.tick(fps)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
  if generating:
    unvisited[0].next()
  pygame.display.update()





