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
class RRT_Map:
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
    self.nodeRad = 0
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
  
  def draw_map(self, obstacles):
    pygame.draw.circle(self.map, self.Green, start, self.nodeRad+5, 0)
    pygame.draw.circle(self.map, self.Green, goal, self.nodeRad+20, 1)
    slef.draw_obs(obstacles)
  
  def draw_path(self):
    pass
  
  def draw_obs(self, obstacles):
    obstaclesList = obstacles.copy()
    while (len(obstaclesList) > 0):
      obstacle = obstaclesList.pop(0)
      pygame.draw.rect(self.map, self.grey, obstacle)
    
  
#method to make random obstacle, add/remove node, add edge to the tree
#checks the collision, find the nearest neighbor
class RRT_Graph:
  def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
    #start coordinates
    (x, y) = start
    self.start = start
    self.goal = goal
    
    #state of if reached the goal
    self.goalFlag = False
    self.maph, selfmapw = MapDimensions
    
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
  
  def make_random_rect(self):
    #make random rectiangle for obstacles
    uppercornerx = int(random.uniform(0,self.mapw-self.obsDim))
    uppercornery = int(random.uniform(0,self.mapw-self.obsDim))
    #return turple of coordinate
    return (uppercornerx, uppercornery)
  
  def make_obs(self):
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
  
  def add_node(self):
    pass
  
  def remove_node(self):
    pass
  
  def add_edge(self):
    pass
  
  def number_of_nodes(self):
    pass
  
  def distance(self):
    pass
  
  def nearest(self):
    pass
  
  def is_free(self):
    pass
  
  def cross_obstacle(self):
    pass
  
  def connect(self):
    pass
  
  def step(self):
    pass
  
  def path_to_goal(self):
    pass
  
  def get_path_coords(self):
    pass
  
  def bias(self):
    pass
  
  def expand(self):
    pass
  
  def cost(self):
    pass
