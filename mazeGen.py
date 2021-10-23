import random

unvisited = []

path = []

x = 10
y = 10
last = 10*10 - 1

class Node:

  def __init__(self, nr):
    self.nr = nr
    self.visited = False
  
  # going to next unvisited node
  def next(self):
    self.neighbourNodes = self.findNeighbours()
    if not neighbourNodes:
      backtrack()
      return

    self.visited = True
    unvisited.remove(self)
    path.append(self)

    


  def findNeighbours(self):
    neighbours = []
    nodeNeighbours = []

    # possible adjacent neighbours, accounting for bounds
    if self.nr % x != 0:
      neighbours.append(nr-1)
    elif self.nr % x != (x-1):
      neighbours.append(nr+1)
    if last-self.nr >= x:
      neighbours.append(nr+x)
    elif self.nr - x >= 0:
      neighbours.append(nr-x)

    # turning those numbers into nodes
    for node in unvisited:
      if node.nr in neighbours:
        nodeNeighbours.append(node)
        
    return nodeNeighbours

    def chooseNeighbour(self, neighbours):
      index = random.randint(0, len(neighbours))


