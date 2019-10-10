import matplotlib.pyplot as plt
from Map import Map

class State:
    def __init__(self, position, g):
        # init unopened state
        self.checked = False

        # current coordinates
        self.position = position

        # heuristic values
        self.g = g
        self.h = 0
        self.f = 0

    def calculateF(self, goal):
        self.calculateH(goal)
        self.f = self.h + self.g
        return self.f

    def calculateH(self, goal):
        self.h = abs(self.position[0] - goal[0]) + abs(self.position[1] - goal[1])
        return self.h

    def atDestination(self, goal):
        if self.position != goal:
            return False
        return True


def AStarSearch(Map):
    # starting position state
    positionState = State(Map.start, 0)

    # list of opened and closed points
    openList = []
    closedList = []

    # add start to open list
    
    while not state.atDestination:
        pass
    


if __name__ == '__main__':
    Map1 = Map(30, 20, (18, 1), (1, 28))
    plt.imshow(Map1._map)
    plt.show()