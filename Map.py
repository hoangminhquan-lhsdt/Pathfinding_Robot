class Map:
	def __init__(self, row, col, start=(19,0), goal=(0,29)):
		# create 2d array
		self.map = [[0 for x in range(row)] for y in range(col)]

		# set start and goal
		self.start = start
		self.goal = goal
		self.map[self.start[0]][self.start[1]] = 2
		self.map[self.goal[0]][self.goal[1]] = 3

		self.obstacleList = list()
		self.pickupPoints = list()
    
	def addObstacle(self, pointsList):
		for i in pointsList:
			self.obstacleList.append(i)
			self.map[i[0]][i[1]] = 1

	def addPickup(self, pointsList):
		pass

	def printMap(self):
		for i in self.map:
			print(i)

	def isBlocked(self, x, y):
		if (x,y) in self.obstacleList:
			return True
		return False