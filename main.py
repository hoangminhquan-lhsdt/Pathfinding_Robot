import matplotlib.pyplot as plt
from Map import Map
import math

class State:
	def __init__(self, position: (int, int), goal: (int, int), g=0):
		# init unopened state
		self.checked = False

		# current coordinates
		self.position = position

		# parent state
		self.parent = None

		# cost
		self.g = g
		# manhattan distance
		self.h = abs(self.position[0] - goal[0]) + abs(self.position[1] + goal[1])
		# heuristic value
		self.f = self.g + self.h

	def atDestination(self, goal: (int, int)):
		if self.position != goal:
			return False
		return True
'''
def getChildren(pos: (int, int), Map: Map, parentG):
	return [
		State((pos[0]-1,pos[1]), Map.goal, parentG + 1),
		State((pos[0]+1,pos[1]), Map.goal, parentG + 1),
		State((pos[0],pos[1]-1), Map.goal, parentG + 1),
		State((pos[0],pos[1]+1), Map.goal, parentG + 1)
	]
'''
def getChildren(pos: (int, int), Map: Map, parentG):
	result = []
	if pos[0] > 0 and pos[0] < Map._map.__len__()-1:
		result.append(State((pos[0]-1,pos[1]), Map.goal, 0))
		result.append(State((pos[0]+1,pos[1]), Map.goal, 0))
	elif pos[0] == 0:
		result.append(State((pos[0]+1,pos[1]), Map.goal, 0))
	elif pos[0] == Map._map.__len__()-1:
		result.append(State((pos[0]-1,pos[1]), Map.goal, 0))

	if pos[1] > 0 and pos[1] < Map._map[0].__len__()-1:
		result.append(State((pos[0],pos[1]-1), Map.goal, 0))
		result.append(State((pos[0],pos[1]+1), Map.goal, 0))
	elif pos[1] == 0:
		result.append(State((pos[0],pos[1]+1), Map.goal, 0))
	elif pos[1] == Map._map[0].__len__()-1:
		result.append(State((pos[0],pos[1]-1), Map.goal, 0))

	return result
'''
def AStar_Search(Map: Map):
	# opened and closed points
	openList = []
	closedList = []

	# init starting point
	currentPoint = State(Map.start, Map.goal, 0)

	# add starting point
	openList.append(currentPoint)

	while openList.__len__():
		currentPoint = min(openList, key=lambda p: p.f)

		if currentPoint.position == Map.goal:
			path = []
			while currentPoint.parent:
				path.append(currentPoint)
				currentPoint = currentPoint.parent
			path.append(currentPoint)
			return path[::-1]
		
		# remove point from open list
		openList.remove(currentPoint)
		closedList.append(currentPoint)

		for newPoint in getChildren(currentPoint.position, Map, currentPoint.g):
			if newPoint in closedList:
				continue
			
'''
def BFS(Maps: Map):
	queue = []
	queue.append(State(Maps.start, Maps.goal, 0))
	while queue.__len__() > 0:
		currentState = queue.pop()
		print(currentState.position)
		currentState.checked = True
		for neighbor in getChildren(currentState.position, Maps, 0):
			neighbor.parent = currentState
			if neighbor == State(Maps.goal, Maps.goal, 0):
				return neighbor
			if neighbor.checked:
				continue
			queue.append(neighbor)
			neighbor.checked = True


if __name__ == '__main__':
	start = (18,5)
	Map1 = Map(20, 30, start, (1, 18))
	print(BFS(Map1))
	# plt.imshow(Map1._map)
	# plt.axis([0,29,0,19])
	# plt.show()