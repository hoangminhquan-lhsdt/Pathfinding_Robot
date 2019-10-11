import matplotlib.pyplot as plt
from Map import Map
import math

class State:
    def __init__(self, position, goal, g=0):
        # init unopened state
        self.checked = False

        # current coordinates
        self.position = position

        # heuristic values
        self.g = g
        self.h = abs(self.position[0] - goal[0]) + abs(self.position[1] + goal[1])
        self.f = self.g + self.h

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

def Greedy_Search(Map):
	positionState = State(Map.start,Map.goal,0)
	

	while not positionState.atDestination:
		openList = [State]




if __name__ == '__main__':
    Map1 = Map(30, 20, (18, 1), (1, 28))
    plt.imshow(Map1._map)
    plt.show()