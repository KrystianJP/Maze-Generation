import random,time

unvisited = []

path = []

x = 4
y = 4
last = x*y - 1

class Node:

  def __init__(self, nr):
    self.nr = nr
  
  # going to next unvisited node
  def next(self):
    time.sleep(0.5)
    neighbourNodes = self.findNeighbours(self.nr)

    print("current node:", self.nr)
    nodenrs = []
    for node in neighbourNodes:
      nodenrs.append(node.nr)
    print(nodenrs)

    if self in unvisited: # don't do if it had been backtracked to
      unvisited.remove(self)
      path.append(self)

    if not neighbourNodes:
      self.backtrack()
      return

    chosenNeighbour = self.chooseNeighbour(neighbourNodes)
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

  @staticmethod
  def finished():
    print("FINAL PATH")
    nodenrs = []
    for node in path:
      nodenrs.append(node.nr)
    print(nodenrs)

for nr in range(x*y):
  unvisited.append(Node(nr))

unvisited[0].next()



