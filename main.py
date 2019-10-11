import matplotlib.pyplot as plt
from Map import Map
import math

class State:
	def __init__(self, position: (int,int), goal: (int,int), g=0):
		# init unopened state
		self.checked = False

		# current coordinates
		self.position = position

		# heuristic values
		self.g = g
		self.h = abs(self.position[0] - goal[0]) + abs(self.position[1] + goal[1])
		self.f = self.g + self.h
	
	def goU(self):
		temp = list(self.position)
		temp[0] -= 1
		self.position = list(temp)
	def goD(self):
		temp = list(self.position)
		temp[0] += 1
		self.position = list(temp)
	def goL(self):
		temp = list(self.position)
		temp[1] -= 1
		self.position = list(temp)
	def goR(self):
		temp = list(self.position)
		temp[1] += 1
		self.position = list(temp)

	def setPosition(self,p:int):
		self.position = p

	def atDestination(self, goal):
		if self.position != goal:
			return False
		return True


def AStar_Search(Map):
	# starting position state
	positionState = State(Map.start, Map.goal, 0)

	# list of opened and closed points
	openList = []
	closedList = []

	# add start to open list
	openList.append(positionState)

	while not positionState.atDestination:
		# find state with lowest f value
		index = 0
		for i in range(openList.__len__()):
			Fmin = math.inf
			if Fmin > openList[i].f:
				Fmin = openList[i].f
				index = i


def GS_regetOpenList(iMap:Map,positionState:State,resultList:list):
	openList = []
	Nextmove = positionState

	Nextmove.goU

		# Nextmove.setPosition(Nextmove.position[0]+1)
		# if iMap.isBlocked(Nextmove.position[0],Nextmove.position[1]) == False:
		# 	if Nextmove.position != resultList[-1]:
		# 		openList.append(Nextmove.position)
		# Nextmove = positionState
		# Nextmove.position[i] -= 1
		# if iMap.isBlocked(Nextmove.position[0],Nextmove.position[1]) == False:
		# 	if Nextmove.position != resultList[-1]:
		# 		openList.append(Nextmove.position)
	return openList


def Greedy_Search(iMap:Map):
	positionState = State(iMap.start,iMap.goal,0)
	resultList = []
	openList = []
	GS_regetOpenList(iMap,positionState,resultList)
	print(openList)
	pass



if __name__ == '__main__':
	iMap = Map(30, 20,(19,0),(0,29))
	iMap.addObstacle(((1,1),(1,2),(1,3)))
	# plt.imshow(iMap._map)
	# plt.show()


	# Greedy_Search(iMap)

