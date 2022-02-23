"""
  To do mothing planning we also have A* and D* such algorithm. But they are grid-based algorithms
  So mean that they needs to discretiz the world map. As our simulation I think will be better idea to
do consider our input as continuous and also considering to late robort handle unexpected obstacle. More over
RRT does save memory and time while finding the path. So I will stick with learning RRT algo insted of others 
for solving motion planning.
  RRT to solve motion planning problem
  RRT(rapidly exploring random trees) - sampling based
  note: solution is not optimal like A* but we can dealt with path optimization
"""
import random
import math
import pygame

#drawing the map, obstacles and path
class RRTMap:
  #start, goal, map's dimensions, obstacles's dimensions and obscales numbers
  def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
    self.start = start
    self.goal = goal
    self.MapDimensions = MapDimensions
    #map width and map height
    self.Maph, self.Mapw = self.MapDimensions
    
    #window settings by pygame
    self.MapWindowName = 'RRT path planning'
    pygame.display.set_caption(self.MapWindowName)
    self.map = pygame.display.set_mode((self.Mapw, self.Maph))
    self.map.fill((255,255,255))
    self.nodeRad = 2
    self.nodeThickness = 0
    self.edgeThickness = 1
    
    #obstacles
    self.obstacles = []
    self.obsdim = obsdim
    self.obsNumbewr = obsnum
    
    #colors of obstacles
    self.grey = (70, 70, 70)
    self.Blue = (0, 0, 255)
    self.Green = (0, 255, 0)
    self.Red = (255, 0, 0)
    self.white = (255, 255, 255)
  
  def drawMap(self, obstacles):
    pygame.draw.circle(self.map, self.Green, self.start, self.nodeRad+5, 0)
    pygame.draw.circle(self.map, self.Green, self.goal, self.nodeRad+20, 1)
    self.drawObs(obstacles)
  
  def drawPath(self, path):
    for node in path:
      pygame.draw.circle(self.map, self.Red, node, self.nodeRad+3, 0)

  
  def drawObs(self, obstacles):
    obstaclesList = obstacles.copy()
    while (len(obstaclesList) > 0):
      obstacle = obstaclesList.pop(0)
      pygame.draw.rect(self.map, self.grey, obstacle)
    
  
#method to make random obstacle, add/remove node, add edge to the tree
#checks the collision, find the nearest neighbor
class RRTGraph:
  def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
    #start coordinates
    (x, y) = start
    self.start = start
    self.goal = goal
    
    #state of if reached the goal
    self.goalFlag = False
    self.maph, self.mapw = MapDimensions
    
    #structure that allows us to store the node and it's parents
    self.x = []
    self.y = []
    self.parent = []
    
    #append the initial node to the list
    self.x.append(x)
    self.y.append(y)
    self.parent.append(0)
    
    #obstacles
    self.obstacles = []
    self.obsDim = obsdim
    self.obsNum = obsnum
    
    #path
    self.goalstate = None
    self.path = []
  
  def makeRandomRect(self):
    #make random rectiangle for obstacles
    uppercornerx = int(random.uniform(0,self.mapw-self.obsDim))
    uppercornery = int(random.uniform(0,self.maph-self.obsDim))
    #return turple of coordinate
    return (uppercornerx, uppercornery)
  
  def makeobs(self):
    #create obstacles and store in the list
    obs = []
    for i in range(0, self.obsNum):
      rectang = None
      startgoalcol = True
      while startgoalcol:
        upper = self.makeRandomRect()
        rectang = pygame.Rect(upper, (self.obsDim, self.obsDim))
        #check obs is not at the start or goal
        if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
          startgoalcol = True
        else:
          startgoalcol = False
      obs.append(rectang)
    self.obstacles = obs.copy()
    return obs
  
  def add_node(self, n, x, y):
    self.x.insert(n, x)
    self.y.append(y)
  
  def remove_node(self, n):
    self.x.pop(n)
    self.y.pop(n)
  
  def add_edge(self, parent, child):
    #parent: elements, child:index
    self.parent.insert(child, parent)
  
  def remove_edge(self, n):
    self.parent.pop(n)
  
  def number_of_nodes(self):
    return len(self.x)
  
  def distance(self, n1, n2):
    #find distance between two nodes
    (x1, y1) = (self.x[n1], self.y[n1])
    (x2, y2) = (self.x[n2], self.y[n2])
    """
    distanc = root(p_x+p_y)
    p_x = (x1-x2)^2
    p_y = (y1-y2)^2
    """
    px = (float(x1)-float(x2))**2
    py = (float(y1)-float(y2))**2
    return (px+py)**0.5

  def sample_envir(self):
    #random node generation
    x = int(random.uniform(0, self.mapw))
    y = int(random.uniform(0, self.maph))
    return x, y
  
  def nearest(self, n):
    #takes the new added node that was sampled from environment and
    #measured the distance to every node in the tree
    dmin = self.distance(0, n)
    nnear = 0 # hold the closed node inside the loop
    for i in range(0, n):
      if self.distance(i, n) < dmin:
        dmin = self.distance(i, n)
        nnear = i
    return nnear

  
  def isFree(self):
    n = self.number_of_nodes()-1 #total number
    (x, y) = (self.x[n], self.y[n])
    obs = self.obstacles.copy()
    while len(obs) > 0:
      rectang = obs.pop(0)
      if rectang.collidepoint(x, y): #collides with node then not free
        self.remove_node(n)
        return False
    return True
  
  def crossObstacle(self, x1, x2, y1, y2): 
    # check if edge cross obstacle
    obs = self.obstacles.copy()
    while(len(obs) > 0):
      rectang = obs.pop(0)
      for i in range(0 , 101):
        u = i/100
        x = x1 * u + x2 * (1-u)
        y = y1 * u + y2 * (1-u)
        if rectang.collidepoint(x, y):
          return True
    return False
  
  def connect(self, n1, n2):
    (x1, y1) = (self.x[n1], self.y[n1])
    (x2, y2) = (self.x[n2], self.y[n2])
    #check the connection
    if self.crossObstacle(x1, x2, y1, y2):
      self.remove_node(n2)
      return False
    else:
      self.add_edge(n1, n2)
      return True
  
  def step(self, nnear, nrand, dmax = 35):
    d = self.distance(nnear, nrand)
    if d > dmax:
      u = dmax / d
      (xnear, ynear) = (self.x[nnear], self.y[nnear])
      (xrand, yrand) = (self.x[nrand], self.y[nrand])
      """
      x1 = x+n cos(theta)
      y1 = x+n sin(theta)
      """
      (px,py) = (xrand - xnear, yrand - ynear)
      theta = math.atan2(py, px)
      (x, y) = (int(xnear + dmax * math.cos(theta)), int(ynear + dmax * math.sin(theta)))
      self.remove_node(nrand)
      if abs(x - self.goal[0]) < dmax and abs(y - self.goal[1]) < dmax:
        self.add_node(nrand, self.goal[0], self.goal[1])
        self.goalstate = nrand
        self. goalFlag = True
      else:
        self.add_node(nrand, x, y)

  def path_to_goal(self):
    if self.goalFlag:
      self.path = []
      self.path.append(self.goalstate)
      newpos = self.parent[self.goalstate]
      while (newpos != 0):
        self.path.append(newpos)
        newpos = self.parent[newpos]
      self.path.append(0)
    return self.goalFlag
  
  def getPathCoords(self):
    pathCoords = []
    for node in self.path:
      x, y = (self.x[node], self.y[node])

      pathCoords.append((x, y))
    return pathCoords
  
  def bias(self, ngoal):
    n = self.number_of_nodes()
    self.add_node(n ,ngoal[0], ngoal[1])
    nnear = self.nearest(n)
    self.step(nnear, n)
    self.connect(nnear, n)
    return self.x, self.y, self.parent
  
  def expand(self):
    n = self.number_of_nodes()
    x , y = self.sample_envir()
    self.add_node(n, x, y)
    if self.isFree():
      xnearest = self.nearest(n)
      self.step(xnearest, n)
      self.connect(xnearest, n)
    return self.x, self.y, self.parent
  
  def cost(self):
    pass